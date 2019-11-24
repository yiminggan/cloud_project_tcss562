import detector as dc
from Inspector import *
import boto3 
import os

def handler(event, context):
	s3_client = boto3.client('s3')
	# import the module and collect data
	inspector = Inspector()
	inspector.inspectAll()
	inspector.addTimeStamp("frameworkRuntime")
	
	# detector
	bucket = event.get("bucketname")
	key = event.get("filename")

	#image = os.mkdir(os.path.join('/tmp', key))
	image = '/tmp/target.jpg'
	print(image)
	s3_client.download_file(bucket, key, image)
	box, profile = dc.getBox(image)

	inspector.addAttribute("box", str(box))
	inspector.addAttribute("Detector_profile", profile)

	inspector.inspectCPUDelta()
	return inspector.finish()
