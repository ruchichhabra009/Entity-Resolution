import json
import re
from collections import OrderedDict
import sys

def run(filename):
	d = {}
	flipped={}
	i=0
	f = open(filename, 'r')
	for line in f.readlines():
		i = i+1
		mline = line.strip()
		key,value = mline.split(" - ")
		
		last_name = process_key(key,i)
		#print(last_name)
		classes = process_value(value)
		if last_name in d:
			d[last_name].append(classes)
		else:
			d[last_name] = classes
	process_dict(d)
	#json.dump(d, file('cleaned.txt', 'w'))

#to process professor names seperately
def process_key(key,i):
	skey = key.strip()
	lastname = ""
	if len(skey.split()) > 2:
		if ',' in skey:
			lastname,firstname = skey.split(",")
			#print lastname
		else: 
			firstname,middlename,lastname = skey.split()
			#print lastname
	elif ',' in skey:
		lastname,firstname = skey.split(",")
		#print lastname
			# d[lastname] = d.pop(name)
	elif '.' in skey:
		firstname,lastname = skey.split('.')
	elif len(skey.split()) == 2:
		firstname,lastname = skey.split()
	else:
		lastname = skey
		#print lastname
	slastname = lastname.strip().title()
	return slastname

#convert into strings
def process_dict(dict_item):
	#sorted(dict_item,key=dict_item.get)
	database = {}
	for key,value in dict_item.items():
		str1 = []
		for x in value:
			if isinstance(x,list):
				for y in x:
					str1.append(y)	
			else:
				str1.append(x)
		database[key] = str1
	process_courses(database)

#append data into cleaned.txt file
def process_courses(data_item):
	course = {}

	for key, value in data_item.items():
		str2 = "|".join(str(x) for x in value)
		#print str2
		course[key] = str2.lower()
		#print (key,":",str2)
	#query1()
	data = OrderedDict(sorted(course.items()))
	json.dump(data, open('cleaned.txt', 'w'),indent=2)


def process_value(value):
	l=[]
	class_name = value.strip()
	l = class_name.split('|')
	#print l
	return l


if __name__ == '__main__':
	filename = str(sys.argv[1])
	run(filename)
	print("Executed Successfuly and generated cleaned.txt !!!!!")
   
