#https://docs.appdynamics.com/display/PRO42/Application+Model+API
import json
import requests

response = requests.get('http://server:8090/controller/rest/applications?output=JSON', auth=('username@customer1', 'password'))
data = response.json()
machines = set()

print "AppName, Machine, Machineid, Agent Name, TierName, Type, Version"
for app in data:
	appName = app['name']
	#print "App Name:" + appName
	response = requests.get('http://servername:8090/controller/rest/applications/'+appName+'/nodes?output=JSON', auth=('username@customer1', 'password'))
	agents = response.json()
	for agent in agents:
		machines.add(agent['machineName'])
		print appName + "," + str(agent['machineName']) + "," + str(agent['machineId']) + "," + str(agent['name']) + "," + str(agent['tierName'])  + "," + str(agent['agentType']) + "," + str(agent['appAgentVersion'])

#curl -s --user username@customer1:password "http://servername:8090/controller/rest/applications?output=JSON">>agents/$OUTNAME
#curl -s --user username@customer1:password "http://servername:8090/controller/rest/applications/$APP_FORMATTED/nodes" >>agents/agents.xml.$DATE
