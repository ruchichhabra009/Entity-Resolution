import json
import re
from collections import OrderedDict
import enchant
from nltk.corpus import stopwords
import string
from nltk.stem.porter import *
import sys

correct_word = {}
database = {}
filename = str(sys.argv[1])
database_store=json.load(open(filename))
stemmer = PorterStemmer()
similar=[]
q3_dict={}
max_count = 0
count_=[]

def spell_check():
	list_=[]
	i=0
	dict_ = enchant.Dict("en_US")
	database = json.load(open(filename))
	for key,value in database.items():
		course = tokenize_string(value,'|')
		q3_dict[key]=len(course)
		#print(course)
		for each_course in course:
			cleaned_course = clean_course(each_course)
			#print("here:",cleaned_course)
			#print("course:",each_course)
			words = tokenize_string(cleaned_course,' ')
			for word in words:
				# s = (re.findall("(\w+\.)", word))
				# if s:
				# 	word = "introductioz"
				#word = re.sub(r'\&','and',word)
				if word and not word.isspace():
					if dict_.check(word) == False:
						i=i+1
						list_ = dict_.suggest(word)
						check_edit(word,list_)
	#print("num:",i)

#if suggested words have edit distance less than two then that word is replaced with mispelled
#else if there is no word which has edit distance then keep the same word
#else if there are multiple words , fetch only first word

def check_edit(word,list):

	word1='and'
	word = word.strip()
	first_suggested_word = ''
	i=0
	word2='&'
	for each_ in list:
		if edit_distance(word,each_) <= 2:
			if(len(word) == len(each_)):
				i=i+1
				if i==1:
					correct_word[word] = each_.lower()
	#correct_word['Intro.']='introduction'
	correct_word[word2] = word1

#took from internet
def edit_distance(string1, string2):
    length1=len(string1)+1
    length2=len(string2)+1

    content = {}
    for i in range(length1): content[i,0]=i
    for j in range(length2): content[0,j]=j
    for i in range(1, length1):
        for j in range(1, length2):
            cost = 0 if string1[i-1] == string2[j-1] else 1
            content[i,j] = min(content[i, j-1]+1, content[i-1, j]+1, content[i-1, j-1]+cost)

    return content[i,j]

def correct_incorrect():
	for k,v in correct_word.items():
		#print(k)
		# print(k,v)
		find_replace(k.lower(),v)

def find_replace(incorrect,correct):
	#print("inside")
	for key,value in database_store.items():
	
		if incorrect in value:
			new_value = value.replace(incorrect,correct)
			database_store[key] = new_value
		

def clean_course(course_info):
	stop = stopwords.words('english')
	punctuation_ = set(string.punctuation)
	str1 = ''
	#course = ''.join(ch for ch in course_info if ch not in punctuation_)
	for each_word in tokenize_string(course_info,' '):
		if len(each_word)>2:
			each_word = each_word.title()
			each_word = each_word.replace(',', '')
			each_word = each_word.replace(':','')
			each_word = re.sub(r'\&','and',each_word)
			each_word = re.sub(r'\?','',each_word)
			each_word = re.sub('[\s]+',' ',each_word)
			if each_word not in stop:
				str1 = str1 + " " + each_word
	return str1

def tokenize_string(text,delimiter):
	each_words = text.split(delimiter)
	return each_words

def query1():
	q1=[]
	i =0
	for key,value in database_store.items():
		courses = tokenize_string(value,'|')
		for each_course in courses:
			if each_course not in q1:
				q1.append(each_course)
	
	for each in q1:
		i=i+1
		#print (each)
	print("Query 1")
	print("==========================================")
	print("Distinct Courses in the database are ", i)
	print("===========================================")
	# process_query1(q1)
	
# def process_query1(list1):
# 	word=[]
# 	for each_val in list1:
# 		str1 = clean_course(each_val)
# 		word.append(str1.split())
# 	find_similar_word(word)

# def find_similar_word(word_list):
# 	print("in progress")
# 	for each in word_list:
# 		for a in each:
# 			find_edit_distance_word(a,word_list)

# def find_edit_distance_word(word,word_list):
# 	for each in word_list:
# 		for a in each:
# 			if edit_distance(a,word) < 2:
# 				similar.append(a)

# 	print(similar)

def query2(name):
	# q2 = json.load(open('cleaned.txt'))
	firstname,lastname = name.split()
	#print(lastname)
	if lastname in database_store:
		course_info(database_store[lastname])
	else:
		return

def course_info(course_):
	str1 = course_.split("|")
	str1 = sorted(str1)
	str2 = (',').join(str1).title()
	print("Query2")
	print("============================")
	print(str2)
	print("============================")

def query3():
	req_list = []
	#print(q3_dict)
	for key,value in q3_dict.items():
		if value>=5:
			req_list.append(key)
	find_jaccard_distance(req_list)

def find_jaccard_distance(mylist):
	max_count = 0
	prof1='None'
	prof2='None'
	for l in range(len(mylist)):
		for m in range(l + 1, len(mylist)):
			count = compare(mylist[l], mylist[m])
			if max_count < count:
				max_count = count
				prof1 = mylist[l]
				prof2 = mylist[m]
	print("Query 3")
	print("==================================")
	print(max_count,prof1,prof2)
	print("==================================")

def compare(prof1,prof2):
	course1 = database_store[prof1]
	course2 = database_store[prof2]
	count = 0
	list1 = tokenize_string(course1,"|")
	list2 = tokenize_string(course2,"|")
	for each_course1 in list1:
		for each_course2 in list2:
			if each_course1 == each_course2:
				count = count+1
				#print(each_course1)

	#print("here:",count)
	#count_.append(count)
	return count

def dump_data():
	#print("run")
	data = OrderedDict(sorted(database_store.items()))
	for key,value in data.items():
		data[key] = value.title()
	json.dump(data, open('cleaned_corrected.txt', 'w'),indent=2)
	
if __name__ == '__main__':
    spell_check()
    correct_incorrect()
    dump_data()
    query1()
    query2("Mitchel Theys")
    query3()