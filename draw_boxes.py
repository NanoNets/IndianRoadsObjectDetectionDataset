from PIL import Image, ImageDraw
import sys
import xml.etree.ElementTree as ET
import os
import traceback
import random

r_color = lambda: random.randint(0,255)

def get_boxes_from_filepath(filepath):
	tree = ET.parse(filepath)
	root = tree.getroot()
	boxes = []
	for child in root:
		if child.tag == "object":
			box_dict = {}
			child_object = child
			for attribs in child_object:
				if attribs.tag == "name":
					box_dict["name"]=attribs.text
				if attribs.tag == "bndbox":
					for coord in attribs:
						box_dict[coord.tag] = int(coord.text)
			boxes.append(box_dict)
	return boxes

def draw_rectangle(im, coordinates, color, width=1):
	drawing = ImageDraw.Draw(im)
	for i in range(width):
		rect_start = (coordinates[0][0] - i, coordinates[0][1] - i)
		rect_end = (coordinates[1][0] + i, coordinates[1][1] + i)
		drawing.rectangle((rect_start, rect_end), outline = color)
	del drawing
	return im

images = ["images/"+i for i in os.listdir("images") if i.endswith(".png")]


object_names = []
for image_path in images:
	if os.path.exists(image_path.replace("images","annotations/xml").replace("png","xml")):
		boxes = get_boxes_from_filepath(image_path.replace("images","annotations/xml").replace("png","xml"))
		for i in boxes:
			if i["name"] not in object_names:
				object_names.append(i["name"])
color_map = {}
for i in object_names:
	color_map[i] = (r_color(),r_color(),r_color(),100)

for image_path in images:
	im = Image.open(image_path)
	new_name = image_path.replace("images/","")
	if os.path.exists(image_path.replace("images","annotations/xml").replace("png","xml")):
	 	boxes = get_boxes_from_filepath(image_path.replace("images","annotations/xml").replace("png","xml"))
	 	for i in boxes:
	 		im = draw_rectangle(im, [(i["xmin"], i["ymin"]), (i["xmax"], i["ymax"])], color_map[i["name"]], 3)
	 	im.save("annotated2/"+new_name, "PNG")