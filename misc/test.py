import datetime
import ConfigParser

now = datetime.datetime.now()
pnow = now.strftime("%Y%m%d%H%M%S")
print pnow

config = ConfigParser.ConfigParser()
config.read("reportConfigurationFile.cfg")
pairs = config.items('Reports')
for pair in config.items('Reports'):
	print pair[0] + " " + pair[1]

