# Modified version of code found on http://fragments.turtlemeat.com/pythonwebserver.php
# 
import string,cgi,time,appDynamicsViewData,os
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class MyHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		vd = appDynamicsViewData.view()
		if not vd.getParams():
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write("<html><body><p>I couldn't set the params, check the code.")
			return			

		splitpath = self.path.split("/")
		#print "  Path is " + self.path
		#print "  Path split is " + str(splitpath)
		#print "  Splitpath length =" + str(len(splitpath))
		if len(self.path) > 200:
			self.wfile.write('<html><body>A path of more than 200? That is suspicious. I am shutting down the server.</html>')
			sys.exit("Is a path of more than 200 really needed? Shutting down...")
		try:
			#some simple checks for what to do. 
			if self.path == "/" or self.path == "/apps" or self.path == "/apps/":
				# display the apps from AppDynamics
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				self.wfile.write("<html><body><p>Here is a list of applications in AppDynamics. You can view either the Nodes or Tiers<br>")
				self.wfile.write("<a href=\"/reports\">Click here for the reporting interface.</a><br>")
				self.wfile.write(vd.displayAppNames("html"))
				self.wfile.write("</html>")
				return	
			elif len(splitpath) == 4 and self.path.startswith('/app/') and self.path.endswith('tiers'):
				# Dispay the tiers in an app
				#print 'Running /app/<tiers>!!!'
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				self.wfile.write("<html><body><p>Tiers in " + splitpath[2]+"<br>")
				self.wfile.write(vd.displayTiers(splitpath[2],"html"))
				self.wfile.write("</html>")
				return	
			elif len(splitpath) == 5 and self.path.startswith('/app/')and self.path.endswith('nodes'):
				# Display the nodes in a tier
				#print 'Running /app/<app>/<tier>/nodes!!!'
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				self.wfile.write("<html><body><p>Nodes in App-Tier  " + splitpath[2]+"-"+splitpath[3]+"<br>")
				self.wfile.write(vd.displayNodesInTier(splitpath[2],splitpath[3],"html"))
				self.wfile.write("</html>")
				return	
			elif len(splitpath) == 4 and self.path.startswith('/app/')and self.path.endswith('nodes'):
				# Display the nodes in an app
				#print 'Running /app/<app>/nodes!!!'
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				self.wfile.write("<html><body><p>Tiers in " + splitpath[2]+"<br>")
				self.wfile.write(vd.displayNodes(splitpath[2],"html"))
				self.wfile.write("</html>")
				return	

			elif len(splitpath) == 4 and self.path.startswith('/app/') and self.path.endswith('healthrules'):
				# show the healthrules for an app. 
				#print 'Running /app/<app>/healthrules!!!'
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				self.wfile.write("<html><body><p>Health Rules for " + splitpath[2]+"<br>")
				self.wfile.write(vd.displayHealthRules(splitpath[2],"html"))
				self.wfile.write("</html>")
				return	

			elif len(splitpath) == 4 and self.path.startswith('/app/') and self.path.endswith('policies'):
				#print 'Running /app/<app>/policies!!!'
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				self.wfile.write("<html><body><p>Policies for " + splitpath[2]+"<br>")
				self.wfile.write(vd.displayPolicies(splitpath[2],"html"))
				self.wfile.write("</html>")
				return	

			elif len(splitpath) == 4 and self.path.startswith('/app/') and self.path.endswith('businesstransactions'):
				#print 'Running /app/<app>/businesstransactions!!!'
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				self.wfile.write("<html><body><p>Business Transactions for " + splitpath[2]+"<br>")
				self.wfile.write(vd.displayBT(splitpath[2],"html"))
				self.wfile.write("</html>")
				return	

			elif self.path == '/reports' or self.path == '/reports/':
				#print 'Running reports!!!'
				# Create a new report. 
				# show what reports are available, give form to give time in minutes.
				# Give links to retreive reports. 	
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				self.wfile.write("<html><body>Reports availble to create")
				# Instead of having this being hardcoded, get a list of availble reports from a file:
				appReports = vd.getAppReports();
				self.wfile.write("<table border=1>");
				for ap in appReports:
					self.wfile.write("<tr><td colspan=\"2\" align=center>Create a report for " + ap[1])
					self.wfile.write("<tr><td><form action=\"/reportcreation/"+ap[0]+"\">")
					self.wfile.write("Mins before now:<input type=\"text\" name=mins value=\"60\" maxlength=\"4\" size=\"4\">")
					self.wfile.write("<td><a href=\"/listReports/"+ap[0]+"\">Old Reports</a>")
					self.wfile.write("<tr><td align=center><input type=\"submit\" value=\"Submit\"><td></form>")
				self.wfile.write("</table>");
				self.wfile.write("</html>")
				return	

			elif self.path.startswith('/reportcreation/'):
				#print 'Running /reportcreation/<app>?mins=##'
				checktext=""
				checkboolean = True
				appMin = splitpath[2].split("?")
				mins = appMin[1].split("=")
				passedApp = appMin[0]
				#Check for appname in config
				#Check if a number was passed
				#Check if referer was correct
				if not os.path.isfile("urls/"+passedApp):
					checktext = "Application report template not found. " + "urls/"+passedApp
					checkboolean = False
				try:
					val = int(mins[1])
				except:
					checktext = checktext + " Was a positive number of minutes submitted?" 
					checkboolean = False

				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				self.wfile.write("<html><body>"+checktext)
				if checkboolean:
					fileCreated =  vd.createReport(passedApp,mins[1])
					self.wfile.write("Report name is: <a href=\"/" + fileCreated+"\">" + fileCreated+ "</a><br>")
				else:
					self.wfile.write("The Report couldn't be created because it didn't receive a valid report name or timeframe.<br>")
					self.wfile.write("Or because it didn't come from the form, (if that check is still enabled.)<br>.")
					self.wfile.write("<a href=\"/reports\">Reports</a><br><br>")
					self.wfile.write("This ensures unwanted reports are not run by hitting the back button or something.")
				self.wfile.write("</html>")
				return	

			elif self.path.startswith('/listReports/'):
				appName=splitpath[2]
				mypath="archive/"+appName
				self.wfile.write("<html><body>")
				onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
				self.wfile.write("List of files for " + appName +"-- <br>")
				for ofile in onlyfiles:
					self.wfile.write("<a href=\"/" + mypath +"/" + ofile + "\">"+ofile+"</a><br>")
				self.wfile.write("</body></html>")
				return
				

		except Exception, e:
			self.send_error(500,'Something bad happened in the code. It is probably Jon\'s fault <br> %s' % self.path)
			print "Exception is: " + str(e)
		
		# If the above doesn't work an html can be served.
		try:
			if self.path.endswith(".html"):
				f = open(self.path)
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
				return
			if self.path.startswith("/archive/") and self.path.endswith(".zip"):
				print "Trying to serve file: "+self.path
				cur = os.path.dirname(os.path.abspath(__file__))
				f = open(cur + os.sep + self.path, 'rb')
				self.send_response(200)
				self.send_header("Content-type", "application/octet-stream")
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
				return
		except IOError, e:
			self.send_error(404,'What were you thinking?!? File or activity might not have been found: %s' % self.path)
			print "IOError exception is- " + str(e)
		
	def do_POST(self):
		global rootnode
		try:
			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			if ctype == 'miltipart/form-data':
				query=cgi.parse_multipart(self.rfile,pdict)
			self.send_response(301)
			
			self.end_headers()
			upfilecontent = query.get('upfile')
			print "filecontent", upfilecontent[0]
			self.wfile.write("<HTML>POST OK.<BR><BR>");
			self.wfile.write(upfilecontent[0]);
			self.wfile.write("<HTML>POST Works. But so what?</HTML>")
		
		except:
			pass

def main():
	try:
		server = HTTPServer(('', 8899), MyHandler)
		print 'started httpserver...'
		server.serve_forever()
	except KeyboardInterrupt:
		print '^C received, shutting down server'
		server.socket.close()

if __name__ == '__main__':
	main()

