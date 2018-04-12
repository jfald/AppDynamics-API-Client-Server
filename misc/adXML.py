import requests
from xml.dom.minidom import parse, parseString
import xml.dom.minidom

class ADXMLParser:
	def __init__(self):
		self.CurrentData = ""
		self.name = ""
		self.ruleType = ""
		self.enabled = ""
		self.durationMin = ""
		self.waitTimeMin = ""
		self.conditionValueType = ""
		self.conditionValue = ""
		self.operator = ""
		self.logicalMetricName = ""
	
	def getHealthRules(self,appName):
		#url = 'http://'+self.server+':'+self.port+'/controller/healthrules/'+appName
		url = 'http://vaausappmon240.aac.va.gov:8090/controller/healthrules/'+appName
        	response = requests.get(url,auth=("restapi@customer1", "Restful"))
		#xml.sax.parse(response)	
		print "Got the response, hopefully!!"
		## may need to use this instead?
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
			

if __name__ == "__main__":
        print "Running locally."
	adp = ADXMLParser()
	adp.getHealthRules("FSC-Prod")
