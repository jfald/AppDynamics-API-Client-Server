# use the conn.cfg file to run this.

import appDynamicsAPIClient
import ConfigParser
from misc import CreateReport


class view:
	def __init__(self):
		self.server = ""
		self.port = ""
		self.user = ""
		self.pw = ""
		self.dataSet = False
		self.apiClient = None
		self.parmFile = "conn.cfg"
		self.reportConfigFile = "reports.cfg"
	
	# Create the appDynamicsAPIClient object with the params
	# Variables used incase you don't want to use params. 
	def setAPIClient(self,server,port,user,pw):
		if (not self.dataSet):
			print "Data has not been set!"
			return False
		self.apiclient=appDynamicsAPIClient.appDynamicsAPIClient(server,port,user,pw)
		return True

	#This will get the Params and then call setAPIClient
	def getParams(self):
		config = ConfigParser.ConfigParser()
		config.read(self.parmFile)
		self.server = config.get('AD', 'server')
		self.port = config.get('AD', 'port')
		self.user = config.get('AD', 'user')
		self.pw = config.get('AD', 'pw')
		self.dataSet = True
		success = self.setAPIClient(self.server,self.port,self.user,self.pw)
		return success

	# Get AppNames
	def displayAppNames(self,outputType):
		appNames = self.apiclient.getApplicationNames()
		if outputType == "html" and appNames is not None:
			returnString = "<p><table border=1><tr><th>App<th>Tiers<th>Node<th>Health Rules<th>Policies"
			for name in appNames:
				returnString += "<tr><td>"+name+"<td><a href='/app/"+name+"/tiers'>Tiers</a><td><a href='/app/"+name+"/nodes'>Nodes</a><td><a href='/app/"+name+"/healthrules'>Rules</a><td><a href='/app/"+name+"/policies'>Policies</a>"
			return returnString+"</table>"
		else:
			for name in appNames:
				print name
		return

	# Get TierNames
	def displayTiers(self,app,outputType):
		tiers = self.apiclient.getTiers(app)
		if outputType == "html":
			returnString = "<p><table border=1><tr><th>Name<th>Type<th>agentType<th># of nodes<th>link"
			for name in tiers:
				returnString += "<tr><td>"+name[0]+"<td>"+name[1]+"<td>"+name[2]+"<td>"+name[3]+"<td><a href='/app/"+app+"/"+name[0]+"/nodes'>Nodes</a>"
			returnString += "</table>"
			return returnString
		else:
			print "Name,Type,Agent Type,# of nodes"
			for name in tiers:
				print name[0]+","+name[1]+","+name[2]+","+name[3]
		return

	# Get NodesInTier
	def displayNodesInTier(self,app,tier,outputType):
		nodes = self.apiclient.getNodesInTier(app,tier)
		if outputType == "html":
			returnString = "<p><table border=1><tr><th>Name<th>Type<th>Agent Type<th>Agent Version"
			for node in nodes:
				returnString += "<tr><td>"+node[0]+"<td>"+node[1]+"<td>"+node[2]+"<td>"+node[3]
			return returnString + "</table>"
		else:
			for node in nodes:
				print node[0]+","+node[1]+","+node[2]+","+node[3]
		return

	# Get Nodes
	def displayNodes(self,app,outputType):
		nodes = self.apiclient.getNodes(app)
		if outputType == "html":
			returnString = "<p><table border=1><tr><th>Name<th>Machine ID<th>Machine Name<th>Tier<th>Agent Type<th>Agent Version"
			for node in nodes:
				returnString += "<tr><td>"+node[2]+"<td>"+node[1]+"<td>"+node[0]+"<td>"+node[3]+"<td>"+node[4]+"<td>"+node[5]
			return returnString + "</table>"
		else:
			for node in nodes:
				print node[2]+","+node[1]+","+node[0]+","+node[3]+","+node[4]+","+node[5]
		return
	
	# Get Business Transactions
	def displayBT(self,app):
		bts = self.apiclient.getBT(app)
		if outputType == "html":
			returnString = "<p><table border=1><tr><th>Tier<th>Entry Point Type<th>Internal Name<th>Name"
			for bt in bts:
				returnString += "<tr><td>"+bt[0]+"<td>"+bt[1]+"<td>"+bt[2]+"<td>"+bt[3]
				
			return returnString + "</table>"	
		else:
			for bt in bts:
				print bt[0]+","+bt[1]+","+bt[2]+","+bt[3]
		return

	# get Health Rules
	# name, type, enable, duration-min, wait-time-min, condition-value-type, condition-value, operator, logical-metric-name
	def displayHealthRules(self,app,outputType):
		healthRules = self.apiclient.getHealthRules(app)
		if outputType == "html":
			returnString = "<p><table border=1><tr><th>Name<th>Type<th>Enabled<th>Duration in Minutes<th>Wait Time in Minutes<th>Condition Type<th>Condition Value<th>Operator<th>Logical Metric Name"
			for hr in healthRules:
				returnString += "<tr><td>"+hr[0]+"<td>"+hr[1]+"<td>"+hr[2]+"<td>"+hr[3]+"<td>"+hr[4]+"<td>"+hr[5]+"<td>"+hr[6]+"<td>"+hr[7]+"<td>"+hr[8]
				
			return returnString + "</table>"
		else:
			#I need to change this right?
			print name[0]+","+name[1]+","+name[2]+","+name[3]+","+name[4]+","+name[5]+","+name[6]+","+name[7]+","+name[8]
		return
		
	# get Health Rules
	# name, type, enable, duration-min, wait-time-min, condition-value-type, condition-value, operator, logical-metric-name
	def displayPolicies(self,app,outputType):
		policies = self.apiclient.getPolicies(app)
		if policies is None:
			return "No policies found"	
		if outputType == "html":
			returnString = "<p><table border=1><tr><th>Enabled<th>Name<th>Action<th>Event Types<th>Item(s)"
			for po in policies:
				returnString += "<tr><td>"+po[0]+"<td>"+po[1]+"<td>"+po[2]+"<td>"+po[3]+"<td>"+po[4]
				
			return returnString + "</table>"
		else:
			for po in policies:
				print  po[0]+",\""+po[1]+"\",\""+po[2]+"\",\""+po[3]+"\""
				
		return
	def getAppReports(self):
		config = ConfigParser.ConfigParser()
		config.read(self.reportConfigFile)
		pairs = config.items('Reports')
		return pairs

	def createReport(self,app,mins):
                interval=mins;
		cr = CreateReport.CreateReport(self.user, self.pw, app, interval)
                cr.getData();
                return cr.zipOutput()

# Main part of program if run locally--
if __name__ == "__main__":
	myview = view()
	myview.getParams()	
	myview.setAPIClient("controllername","8090","username@customer1","password")
	#myview.displayAppNames()
	#myview.displayPolicies("appName","html")
	print myview.createReport("appName","60")
	
