#https://docs.appdynamics.com/display/PRO42/Application+Model+API
# This is the client that actaully connects to the API
# It expects the details in the __init__ function
# If you want to test out functions here then look at the __main__ function, otherwise this is meant to be called by other python scripts/functions

import json
import requests
from xml.dom.minidom import parse, parseString
import xml.dom.minidom

class appDynamicsAPIClient:
	def __init__(self,server,port,user,pw):
		self.server = server
		self.port = port
		self.user = user
		self.pw = pw
		self.applications = []

	# get list of application names
	def getApplicationNames(self):
		url = "http://"+self.server+":"+self.port+"/controller/rest/applications?output=JSON"
		response = requests.get(url, auth=(self.user, self.pw))	
		data = response.json()
		returnAppNames=[]
		for d in data:
			returnAppNames.append(str(d['name']))
		return returnAppNames

	# Using the appName get the list nodes for that application.
	# Returns the machineName, id, node name, tier name, agent type, agent version
	def getNodes(self, appName):
		response = requests.get('http://'+self.server+':'+self.port+'/controller/rest/applications/'+appName+'/nodes?output=JSON', auth=(self.user, self.pw))
		nodes = response.json()
		nodeList = []
		for node in nodes:
			nodeList.append([str(node['machineName']),str(node['machineId']),str(node['name']),str(node['tierName']),str(node['agentType']), str(node['appAgentVersion'])])
		return nodeList
			
	# Using the appName get the list business transactions for that application.
	def getBT(self, appName):
		response = requests.get('http://'+self.server+':'+self.port+'/controller/rest/applications/'+appName+'/business-transactions?output=JSON', auth=(self.user, self.pw))
		nodes = response.json()
		nodeList = []
		for node in nodes:
			nodeList.append([str(node['tierName']),str(node['entryPointType']),str(node['internalName']),str(node['name'])])
		return nodeList

	# Using the appName get the list tiers for that application.
	# Returns the tier name, type, agentType, number of nodes 
	def getTiers(self, appName):
		url = 'http://'+self.server+':'+self.port+'/controller/rest/applications/'+appName+'/tiers?output=JSON'
		response = requests.get(url, auth=(self.user, self.pw))
		tiers = response.json()
		tiersList = []
		for tier in tiers:
			tiersList.append([str(tier['name']),str(tier['type']),str(tier['agentType']),str(tier['numberOfNodes'])])
		return tiersList
			
	# Using the appName and tierName, get a list of nodes for that tier
	# Returns the tier name, type, agentType, number of nodes 
	def getNodesInTier(self, appName, tierName):
		response = requests.get('http://'+self.server+':'+self.port+'/controller/rest/applications/'+appName+'/tiers/'+tierName+'/nodes?output=JSON', auth=(self.user, self.pw))
		tiers = response.json()
		tiersList = []
		for tier in tiers:
			tiersList.append([str(tier['name']),str(tier['type']),str(tier['agentType']),str(tier['appAgentVersion'])])
		return tiersList
			
	# Using the appName get the health rules
	# This is only available as XML data
	# Data returned is something like-- name, type, enable, duration-min, wait-time-min, condition-value-type, condition-value, operator, logical-metric-name
	def getHealthRules(self,appName):
		url = 'http://'+self.server+':'+self.port+'/controller/healthrules/'+appName
		response = requests.get(url,auth=("restapi@customer1", "Restful"))
		DOMTree = xml.dom.minidom.parseString(response.text)
		collection = DOMTree.documentElement
		healthRules = collection.getElementsByTagName("health-rule")
		hrList = []
		for hr in healthRules:
			name = hr.getElementsByTagName('name')[0]
			ruleType = hr.getElementsByTagName('type')[0]
			enabled = hr.getElementsByTagName('enabled')[0]
			durationMin = hr.getElementsByTagName('duration-min')[0]
			waitTimeMin = hr.getElementsByTagName('wait-time-min')[0]
			conditionValueType = hr.getElementsByTagName('condition-value-type')[0]
			conditionValue = hr.getElementsByTagName('condition-value')[0]
			operator = hr.getElementsByTagName('operator')[0]
			logicalMetricName = hr.getElementsByTagName('logical-metric-name')[0]
			hrList.append([name.childNodes[0].data, ruleType.childNodes[0].data, enabled.childNodes[0].data, durationMin.childNodes[0].data, waitTimeMin.childNodes[0].data, conditionValueType.childNodes[0].data, conditionValue.childNodes[0].data,operator.childNodes[0].data,logicalMetricName.childNodes[0].data])
		return hrList

	# Using the appName get the policies
	# This is only available as XML data
	# Data returned is something like-- name, type, enable, duration-min, wait-time-min, condition-value-type, condition-value, operator, logical-metric-name
	def getPolicies(self,appName):
		url = 'http://'+self.server+':'+self.port+'/controller/policies/'+appName
		response = requests.get(url,auth=("restapi@customer1", "Restful"))
		try:
			policies = response.json()
		except:
			return
		policyList = []
		awt = [] 
		eft = []
		enft = []
		for po in policies:
			for tempawt in po['actionWrapperTemplates']:
				awt.append(str(tempawt['actionTag']))
			for tempeft in po['eventFilterTemplate']['eventTypes']:
				#print tempeft
				eft.append(tempeft)
			for tempenft  in po['entityFilterTemplates']:
				enft.append(str(tempenft['entityType']))
			policyList.append([str(po['enabled']),str(po['name']),", ".join(awt),", ".join(eft),", ".join(enft)]);
			awt = []
                	eft = []
                	enft = []
		return policyList
		
		
if __name__ == "__main__":
	print "Running locally."
	apiclient=appDynamicsAPIClient("controllername","8090","username@customer1","password")
	# Get AppNames
	print "App Names"
	appNames=apiclient.getApplicationNames()
	for ap in appNames:
		print ap

	# Get NodeNames
	print "Node Names"
	nodeNames=apiclient.getNodes("appName")
	for node in nodeNames:
		print node

	# Get TierNames
	print "Tier Names"
	tierNames=apiclient.getTiers("appName")
	for tier in tierNames:
		print tier

	# Get NodesInTier
	print "Nodes In Tier"
	nodeNames=apiclient.getNodesInTier("appName","Tier Name")
	for node in nodeNames:
		print node

	# Get NodesInTier
	print "Policies"
	policiesList=apiclient.getPolicies("appName")
	for po in policiesList:
		print po



