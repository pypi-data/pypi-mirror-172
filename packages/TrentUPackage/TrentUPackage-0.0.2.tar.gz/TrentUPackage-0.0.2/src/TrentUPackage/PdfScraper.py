import PyPDF2
import re
import time
import os
import io
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options

#Gets cwd so that on any machine it will download the file directly to 
PDF_Directory = os.getcwd() + "\\TrentUAC"

#changing the options to allow for chrome to download the file to the CWD instead of opening it
#adapted from https://stackoverflow.com/questions/53998690/downloading-a-pdf-using-selenium-chrome-and-python
options = Options()
options.set_preference("pdfjs.disabled", True)
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.download.dir", PDF_Directory)
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")


#Instead of having a full chrome install we can use this to launch come
#append the defined options to chrome when opening
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),options=options)

#Static URL of the web page we are scraping, This shouldn't ever change
url = 'https://www.trentu.ca/registrar/academic-calendar/undergraduate-calendar'

#Launches the url and gives a few seconds to process. 
driver.get(url)
time.sleep(3)
#using the xpath even when the PDF gets updated the button will still lead to the new one every time
driver.find_element('xpath', '//*[@id="block-system-main"]/div/div/div/div/p[1]/a').click()
time.sleep(3)
driver.close()
#this will delete the old instance of the file and rename the new one appropriately

for file in os.listdir(PDF_Directory):
    if "TrentUAC.pdf" in file:
        os.remove(PDF_Directory + "\\" + file)

for file in os.listdir(PDF_Directory):
    if "Undergrad" in file:
        os.rename(PDF_Directory + "\\" + file, PDF_Directory + "\\" + "TrentUAC.pdf")
        
# Open the pdf file
pdf_Original = PyPDF2.PdfFileReader(os.getcwd() + '\\TrentUAC\\TrentUAC.pdf', strict=False)

# Get number of pages to ensure we iterate the entire pdf (breaking after a few 100 pages otherwies)
numPages = pdf_Original.getNumPages()

#defined strings to search for both a string and keyword
title_String = "Bachelor of Science Program in Computer Science"
narrow_String = "single-major"
#flag used to cut the leading information before the desired content
head_Flag = False

#this loop will iterate over the maximum number of pages 
#looking for the a match of both the title_String and narrow_string. If successfull
#save that pages text to a file to narrow down the pdf size to only a few pages
#this loop also utilitizes the print function to print to a text file instead of write.(Educational)
for i in range(0, numPages):
    pdf_Page_Object = pdf_Original.getPage(i)
    pdf_Page_Text = pdf_Page_Object.extractText()
    #searching two strongs to try and narrow down the information
    if re.search(title_String,pdf_Page_Text):
        if re.search(narrow_String, pdf_Page_Text):
            append_Text = io.open(os.getcwd() + "\\TrentUAC\\UAC_CS.txt", "w")
            #Remove all ascii characters to only get text
            print(pdf_Page_Text.encode("ascii", "ignore"), file=append_Text)
            append_Text.close()

#This loop will further narrow down the input information removing all the un-nessisary data before
#the start of the keyword defined in narrow_String. Afterwords appending the words to the text file
#It will also check for \n character which denote a newline and remove them, but also adding the
#newline to the new file for readbility and further processing.            
with open(os.getcwd() + "\\TrentUAC\\UAC_CS.txt", "r") as input_File, open(os.getcwd() + "\\TrentUAC\\Formatted_UAC.txt", "w") as output_File:
    for line in input_File:
        for word in line.split():
            #create a flag to cut all the leading information off the text to further
            #narrow down the content
            if narrow_String in word:
                head_Flag = True
            if head_Flag == True:
                if "\\n" in word:
                    output_File.write("\n")
                output_File.write(word.replace("\\n", "") + " ")