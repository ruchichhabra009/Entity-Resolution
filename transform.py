import urllib.request
from bs4 import BeautifulSoup
import csv
import time
import codecs

def getHTML():

	url = "https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions"
	html = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(html,'html.parser')
	soup.encode('utf8')
	soup.prettify()
	extract_info(soup)	

def extract_info(page):

	csv_data = page.find_all("table")
	required_table = csv_data[1].find_all("tr")
	store={}
	headers = []
	j=0
	values=[]
	Database=[]
	for row in required_table:
		header = row.findAll("th")
		if header:
			for c in header:
				j=j+1
				if j<=6:
			
					headers.append(c.get_text())
			Database.append(headers)
			
		i=0
		first = row.findAll("td")
		if first:
			for v in first:
				i=i+1
				if(i==1):
					key=v.get_text().replace('!','').strip()
					vkey = key[3:]
					values.append(vkey)
					print(vkey)
		
				if(i==2):
				
					str1,str2=v.get_text().split(',')
					year = str2.strip()[:4]
					values.append(year)
				
				if(i==3):
				
					str1,str2 = v.get_text().split('!')
					wining_team = str1.strip()
					values.append(wining_team)
				
				if(i==4):
				
					str1,str2=v.get_text().split('!')
					score = str2.strip()
					values.append(score)
					print(score)
				if(i==5):
				
					str1,str2=v.get_text().split('!')
					loosing_team=str1.strip()
					values.append(loosing_team)
				
				if(i==6):
					
					str1,str2=v.get_text().split('!')
					venue=str1.strip()
					values.append(venue)
					
			Database.append(values)
			values=[]

	insertCSV(Database)
	

def insertCSV(data):
	content = [[cell for cell in row] for row in data]
	open_file = codecs.open('result.csv','wb','utf8')
	table_writer = csv.writer(open_file)
	table_writer.writerows(content)
	open_file.close()
	

if __name__ == '__main__':
    getHTML()
