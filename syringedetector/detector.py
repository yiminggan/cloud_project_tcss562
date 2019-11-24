import cv2
import numpy as np
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-c', '--config',default='custom/yolov3-tiny.cfg')
ap.add_argument('-w','--weights',default='custom/yolov3-tiny_100000.weights')
ap.add_argument('-cl','--classes',default='custom/custom/object.names')
args = ap.parse_args()


#image_path = "custom/IMG_0135.jpg"
#img = cv2.imread(image_path)

net = cv2.dnn.readNet(args.weights, args.config)
conf_threshold = 0.5
nms_threshold = 0.4

def getOutputsNames(net):
	layersNames = net.getLayerNames()
	return [layersNames[i[0]-1] for i in net.getUnconnectedOutLayers()]

def getBox(image):
	image = cv2.imread(image)
	blob = cv2.dnn.blobFromImage(image, 1.0/255.0, (416,416),[0,0,0], True, crop=False)
	
	Width = image.shape[1]
	Height = image.shape[0]
	net.setInput(blob)
	outs = net.forward(getOutputsNames(net))

	class_ids = []
	confidences = []
	boxes = []
	for out in outs:
		for detection in out:
			scores = detection[5:]
			class_id = np.argmax(scores)
			confidence = float(scores[class_id])
			if confidence > 0.5:
				center_x = int(detection[0]*Width)
				center_y = int(detection[1]*Height)
				w = int(detection[2]*Width)
				h = int(detection[3]*Height)
				x = int(center_x - w/2)
				y = int(center_y - h/2)
				class_ids.append(class_id)
				confidences.append(confidence)
				boxes.append([x,y,w,h])

	indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

	box=[]
	if len(indices)!= 0:
		i = indices[0]
		i = i[0]
		box = boxes[i]
	
	t,_ = net.getPerfProfile()
	profile_str = 'Inference time: %.2f ms' % (t*1000.0/cv2.getTickFrequency())

	return box, profile_str

#box, profile = getBox(img)
#print(str(box))
#print(profile)
