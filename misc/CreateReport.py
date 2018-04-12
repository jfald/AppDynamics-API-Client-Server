#https://docs.appdynamics.com/display/PRO42/Application+Model+API
import json
import requests
import datetime
import zipfile
import os

##Get incoming variables of 
# time-range-type
# And duration-in-mins
# OR start-time
# OR end-time

class CreateReport:
	def __init__(self, user="username@customer1", pw="password", appName="app", interval="60"):
		self.user = user
		self.pw = pw
		self.apiClient = None
		self.interval = interval
		self.appName = appName
		
	#Read the file that has the urls 
	#Add time to url
	#call the writeToOutFile as approprite
	def getData(self):
		#Pass user and password too?
		#Read from file each line should be a url to retrieve
		nbrLines=0
		nodeName = ""

		with open("urls/"+self.appName) as f, open(self.appName+".csv", 'a') as o:
			o.write("Node Name,Metric Name,TimeStamp,min,max,sum,value,current\n") 
			for urlline in f:
				urlline = urlline.strip()
				#If it is not a comment then it better be a url
				if urlline == "":
					pass
				elif not urlline.startswith('#'):
					# Check for rollup and output
					# rollup=false&output=JSON
					index = urlline.index('?') + 1
					if "rollup=" not in urlline:
						urlline = urlline[:index] + "rollup=false&" + urlline[index:]
					if "output=" not in urlline:
						urlline = urlline[:index] + "output=JSON&" + urlline[index:]
					# Check if number is at the end of the line
					index = urlline.rfind('=') + 1
					numberCheck = urlline[index:]
					if numberCheck.isdigit() :
						urlline = urlline[:index]
						print urlline
					
					urlline = urlline + self.interval

					nbrLines += 1
					response = requests.get(urlline, auth=(self.user, self.pw))
					data = response.json()
					self.writeToOutFile(nodeName,data,o)
				#if it starts with #S then an app name is expected, it will be used as a value in the line for now. 
				elif urlline.startswith('#S'):
					nodeName = urlline[2:]
				#End of if elif
			# end of for urlline in F:
		#end of with open...
		print "Number of URLs:" + str(nbrLines)

	#Hopefully this works. I'm not sure about passing the "o"	
	def writeToOutFile(self,nodeName,data,o):
		#Should I have it in it's own method?		
		for ob in data:
			mn = str(ob['metricName'])
			for metric in ob['metricValues']:
				tstamp=str(metric['startTimeInMillis'])
				fd = datetime.datetime.fromtimestamp(int(tstamp[:10])).strftime('%Y-%m-%d %H:%M:%S')
				o.write(nodeName + "," + mn + "," + fd + "," + str(metric['min']) + "," + str(metric['max']) + "," + str(metric['sum']) + "," + str(metric['value']) + "," + str(metric['current'])+ "\n")

	#This should work for writing to std out. 
	def writeToPrintOut(self,nodeName,data):
		for ob in data:
			mn = str(ob['metricName'])
			for metric in ob['metricValues']:
				tstamp=str(metric['startTimeInMillis'])
				fd = datetime.datetime.fromtimestamp(int(tstamp[:10])).strftime('%Y-%m-%d %H:%M:%S')
				print nodeName + "," + mn + "," + fd + "," + str(metric['min']) + "," + str(metric['max']) + "," + str(metric['sum']) + "," + str(metric['value']) + "," + str(metric['current'])

	#Zip up the output
	def zipOutput(self):
		now = datetime.datetime.now()
		pnow = now.strftime("%Y%m%d%H%M%S")
		zipFileName="archive/"+self.appName+"/"+self.appName+"OutData"+pnow+".zip"
		outFileName=self.appName+".csv"
		with zipfile.ZipFile(zipFileName, 'w') as myzip:
			myzip.write(outFileName)	
		os.remove(outFileName)
		return zipFileName
	
	def createNewReport(self):
	 	self.getData();
		return self.zipOutput()

if __name__ == "__main__":
	doit = CreateReport("username@customer1", "password", "template", "60")
	doit.getData();
	doit.zipOutput()

