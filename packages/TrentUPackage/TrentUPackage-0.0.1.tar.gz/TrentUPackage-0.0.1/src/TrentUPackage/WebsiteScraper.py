#WebsiteParse.py
#Zachary Bricknell
#This script will web scrape a specific web page for trentU to obtain a value pair of 
#Computer science Specializations and the requirements to obtain it. The goal being that
#if additional specializations are added the script would be able to dynamically save that data
#assuming the webpage and html layout remained the same

#Start by defining a linked list to store the data. Each "Node" will have a reference to the 
#next node. The object inside the node will contain two parameters, one for the specialty title
#and the other for the requirements. Using Selenium and a chrome web driver we will install 
#an instance of google chrome and load the desired web page. From there we will find a speciifc
#div tag by searching for a specific div container by its class ID. 
#Appending this to a text file for further data processing. 
#Since it is all in html we will iterate over the data in a linear fassion to find every 
#combination. Since the structure of the website is a header tag (some P tags) and an 
#unordered list we extract the header for the title and every instance of a <li> item for the
#Rquiremnets. Usinga  regex function to strip the html tags we store the data and at the end
#of every list we create and append a node. Continuing untill there are no lines left. 

#comments are intented to be long and descriptive for showing off to non-tech individuals

#------
#-Main-
#------

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
import re


#Linked List Definition

#This is the actual node that will point to the next node
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

#this is the data that we are appending to each node. it will store two strings 
class Specialty:
    def __init__(self, title, requirements):
        self.title = title
        self.requirements = requirements
    
    #this is to be able to quickly print the contents of this class
    def __str__(self):
        return f'Specialty: {self.title}\nRequirements: {self.requirements}'

#This is the linked list with a reference to the first node in the list.
class Specialty_List:
    def __init__(self):
        self.head = None
    
    #definition to append nodes to the linked list in order appending the newest node as
    #the head
    def instert(self, to_Insert):
        new_node = Node(to_Insert)
        new_node.next = self.head
        self.head = new_node
    
    #Iterate over the entire list and print its contents
    def printList(self):
        temp_Node = self.head
        while(temp_Node):
            print(temp_Node.data)
            temp_Node = temp_Node.next

#-----------           
#Main Script
#-----------

#initialize the options for the firefox web driver
options = Options()

#install an instance of chrome to use 
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),options=options)

#Static URL of the web page we are scraping, This shouldn't ever change
url = 'https://www.trentu.ca/cois/programs/degree-computer-science/specializations'

#Launches the url and gives a second to process. 
driver.get(url)

#lxml recomended by BS4
soup = BeautifulSoup(driver.page_source, "lxml")

#Find the required div container by class instead of an ID
div_Container = soup.find_all("div" , {"class": "field-item even"})
specialty_Header_Tag = ["<h1>", "<h2>", "<h3>", "<h4>", "<h5>", "<h6>"]
specialty_List_Tag = "<li>"

specialty_List_Found = False
specialty_Title = ""
specialty_Requirements = ""

#a Regular expression denoting any html tag that may appear <**> 
TAG_RE = re.compile(r'<[^>]+>')

#define remove_tags to use the refular 
def remove_tags(text):
    return TAG_RE.sub('', text)

#printing every line to a text file. This is due to errors reading the div container so 
#we put it in a text file to later iterate over 
with open('..\\..\\data\\Html_text.txt', 'w') as test:
    for html_Tags in div_Container:   
        for html_Line in html_Tags:
            print(html_Line,file=test)
test.close()

#Declare the linked list 
specialty_Linked_List = Specialty_List()

#This loop has a series of operations for cleaning up the data we just created in the text file
#the format on every programs specialty page was <header> <p> <p> <ul> <p> and the data we want
#is only in he header tags coupled with that is below in the unordered list
#we check if any header tag is present(this is due to some pages having different header tags)
#and if so we save that to a string. Following along when we find a <li> take we continuously
#keep appending that line and subsquent lines to a string until theres no more <li> tags. 
#Following that we create a node and append it to the linked list and it searches for the next
#header tag
with open('..\\..\\data\\Html_text.txt', 'r') as test2:
    for line in test2:
        for header in specialty_Header_Tag:
            if header in line:
                specialty_Title = remove_tags(line)
                specialty_List_Search = True
        if specialty_List_Tag in line:
            specialty_Requirements += remove_tags(line)
            specialty_List_Found = True
        elif specialty_List_Found == True:
            temp_Node = Specialty(specialty_Title, specialty_Requirements)
            specialty_Linked_List.instert(temp_Node)
            specialty_List_Found = False                    
test2.close()

driver.close()

#To show the output
specialty_Linked_List.printList()


    