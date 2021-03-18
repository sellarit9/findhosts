import nmap
import json
import os
import requests
import yaml
import random
import time
import json

DD_CLIENT_API_KEY = "<DD-API-KEY"

def sendLogToDatadog(aLog):
	headers = {
	    'Content-Type': 'application/json',
	    'DD-API-KEY': DD_CLIENT_API_KEY,
	}

	data = aLog
	response = requests.post('https://http-intake.logs.datadoghq.com/v1/input', headers=headers, data=data)	

def sendSubnetTraceToDatadog(aStart, aSpanId, aTraceId, aName, aResource):

		# Send the traces.
	headers = {"Content-Type": "application/json"}

	data = [[{
	                "trace_id": aTraceId,
	                "span_id": aSpanId,
	                "name": aName,
	                "resource": aResource,
	                "service": aName,
	                "type": "custom",
	                "start": aStart,
	                "duration": 1,
	                "metrics":{"_sampling_priority_v1":2}
	        }]]

	print(aName)
	print(requests.put("http://localhost:8126/v0.3/traces", data=json.dumps(data), headers=headers))

def sendHostTraceToDatadog(aStart, aParentSpanId, aTraceId, aName, aResource):

		# Send the traces.
	headers = {"Content-Type": "application/json"}

	data = [[{
                "trace_id": aTraceId,
                "span_id": random.randint(1,1000000),
                "name": aName,
                "resource": aResource,
                "service": aName,
                "type": "custom",
                "parent_id": aParentSpanId,
                "start": aStart,
                "duration": 1,
                "metrics":{"_sampling_priority_v1":2}
	        }]]
	print(aName)
	print(requests.put("http://localhost:8126/v0.3/traces", data=json.dumps(data), headers=headers))	


def scan(aSubnet, aTags):
	nm = nmap.PortScanner() # instantiate nmap.PortScanner object

	subnet = aSubnet

	hold = nm.scan(subnet+'/24', arguments='-sn')

	scan = hold['scan']

	print(scan)

	print(len(scan))

	# Create IDs.
	TRACE_ID = random.randint(1,1000000)
	SPAN_ID = random.randint(1,1000000)
	START = int(time.time() * 1000000000)
	if len(scan)>0:
		sendSubnetTraceToDatadog(START,SPAN_ID,TRACE_ID,"subnet-"+subnet,"/"+subnet)

		for item in scan:
			ip = item
			hostnames = scan[item]['hostnames']
			for host in hostnames:
				hostname = host['name']
				print(ip)
				print(hostname)
				print(aTags)
				
				tags = ""

				if len(aTags)>0:

					for tag in aTags:
						tags+=tag+", "			

				tags = tags[:-2]

				print(tags)

				print(json.dumps({
				"subnet":subnet,
		        "ip": ip,
		        "hostname": hostname,
		        "ddsource":"nmap",
		        "service": ip,
		        "ddtags": tags
		    	}))

				sendLogToDatadog(json.dumps({
				"subnet":subnet,
				"ip": ip,
				"hostname": hostname,
				"ddsource":"nmap",
		        "service": ip,
		        "ddtags":tags
				}))

				sendHostTraceToDatadog(START,SPAN_ID,TRACE_ID,hostname,hostname)


def processYaml(aDict):
	print("************")
	print(aDict)
	instances = aDict['instances']
	for instance in instances:
		subnet = instance['subnet']
		tags = instance['tags']
		print(subnet)
		print(tags)
		scan(subnet,tags)


with open("config.yaml", 'r') as stream:
    processYaml(yaml.safe_load(stream))
