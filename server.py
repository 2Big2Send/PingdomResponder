import os, sys, feedparser
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
from daemon import Daemon

ipbind = "" # This allows you to bind to a specific IP address on your server.
port = 8143 # Which port to listen on - don't forget to open this on your firewall.
customProbeIPs = [] # You can add your static IP addresses here for monitoring, the Pingdom ones will be appended to this on start.
pingdomProbeFeed = "https://my.pingdom.com/probes/feed" # Pingdom Probe RSS Feed
log_stdin = "/dev/null" # If you want to write stdin to a file set it here - this must exist.
log_stdout = "/dev/null" # If you want to write stdout to a file set it here.
log_stderr = "/dev/null" # If you want to write stderr to a file set it here.
probeIPs = [] # leave this blank

class PDPRequestHandler(BaseHTTPRequestHandler):
	protocol_version = "HTTP/1.0"
	server_version = "PingdomResponder"
	sys_version = "0.1"

	# Only accept and process a GET request
	def do_GET(self):
		global probeIPs
		clientIP = self.client_address[0]
		# We only want to response nicely to request to root - all other requests return HTTP ERROR 400
		if(self.path == "/"):
			# Check the incoming request
			try:
				probeServerPosition = probeIPs.index(clientIP)
				self.send_response(200)
				self.send_header('Content-Length', 2)
				self.send_header('Content-Type', 'text/plain')
				self.end_headers()
				self.wfile.write("OK") # If you change this message for whatever reason dont forget to change the content-length!
			except ValueError:
				# Probe Server does not exist - throw an error.
				self.send_error(400, "Client not accepted")
		else:
			self.send_error(400, "Path not accepted")

	# Fail all other request types
	def do_HEAD(self):
		self.send_error(400, "Request type not accepted")

	def do_POST(self):
		self.send_error(400, "Request type not accepted")

	def do_PUT(self):
		self.send_error(400, "Request type not accepted")

	def do_DELETE(self):
		self.send_error(400, "Request type not accepted")

	def do_TRACE(self):
		self.send_error(400, "Request type not accepted")


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	pass

class PDResponderDaemon(Daemon):
	def run(self):
		# Start the responder server.
		print "Pingdom Responder Starting on port "+str(port)

		while True:
			try:
				server = ThreadedHTTPServer((ipbind, port), PDPRequestHandler)
				server.serve_forever()
			except:
				print "Error"
				sys.exit(1)


def buildProbeList():
	print "Building list of Pingdom Probe Servers"
	probeServers = feedparser.parse(pingdomProbeFeed)

	# Put the Pingdom Probe IPs into a list.
	for(i, probe) in enumerate(probeServers.entries):
		probeIPs.append(probe['pingdom_ip'])

	# Append any custom IPs to the list.
	for(i, cProbe) in enumerate(customProbeIPs):
		probeIPs.append(cProbe)

	# Check we have some probe servers to listen to.
	if(len(probeIPs) ==0):
		print "There are no probe servers available - Server will not start"
		return False
	else:
		return True

if __name__ == "__main__":
	print "PingdomResponder"
	PDRDaemon = PDResponderDaemon('/tmp/PingdomResponder-daemon.pid', log_stdin, log_stdout, log_stderr)
	if len(sys.argv) >=2:
		if 'start' == sys.argv[1]:
			if buildProbeList():
				print "Starting server"
				PDRDaemon.start()
		elif 'stop' == sys.argv[1]:
			print "Stopping server"
			PDRDaemon.stop()
		elif 'restart' == sys.argv[1]:
			if buildProbeList():
				print "Restarting server"
				PDRDaemon.restart()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)