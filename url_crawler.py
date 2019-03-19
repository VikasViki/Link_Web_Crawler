#Importing bs4 to Use BeautifulSoup method
from bs4 import BeautifulSoup

#Importing requests mnodule in order to get the webpage using the get() method
import requests

#DataFrame method converts the list into a DataFrame
from pandas import DataFrame

#ExcelWriter method converts the dataframe into a excel file with specified name 
from pandas import ExcelWriter

#Getting the keyword from the user that needs to be searched
keyword = input("Enter the Keyword : ")

#Getting the date from the user that needs to be searched for the given keyword
date = input("Enter the Date in D/M/Y format : ")

#Google url to get the links with the entered keyword and date
google = 'https://www.google.com/search?q={0}&source=lmns&tbm=nws'.format(keyword)

#Opening the page by entering the keyword in the url
page = requests.get(google)

#Parsing the html stored in the 'page' varialble and storing it in the BeautifulSoup format
soup = BeautifulSoup(page.text, 'html.parser')

'''
* This Method shows the response of the url in structured HTML format
##print(soup.prettify())

'''

# Creating an empty list to store the dates of the url
date_list = []

# Creating an empty list to store the url for the specifed date of the keyword
url_list = []

# Extracting all the div's witg class 'g' from the page
div = soup.find_all('div', class_ = 'g')

# Extracting the URL link's and dates from the div

for ele in div: # Iterating through each individual div of the page
    # Extracting all dates and URL link's from the page
    for date_from_webpage in ele.find_all('div', class_ = 'slp'): # Iterating through each date from the page
        date_of_url = date_from_webpage.get_text().split('-')[1]
        '''
            This line will print each individual date of the link from the webpage
            print('Link Date\t\t', date_of_url.strip())
        '''
        # Appending the url link to the list only if the published date of the URL
        # is same as the date entered by the user
        if date_of_url.strip() == date.strip():
            #Extracting all the links from the current div
            for link_from_webpage in ele.find_all('a'):
                
                #Extracting URL from the link
                url = link_from_webpage.get('href')[7:].split('&')
                '''
                    This line will print the URL of the links
                    print('URL Link\t\t', url[0])
                '''

                # If the URL is not already in the list then the current URL and Date
                # is added to the list's respectively
                if url not in url_list:
                    url_list.append(url[0])
                    date_list.append(date_of_url)
'''
    This lines will print the dates and URL's extracted from the webpage
    print('\n\n\t\t',date_list)
    print('\n\n\t\t',url_list)
'''

# Creating a DataFrame using date_list and url_list
df = DataFrame({'Date':date_list,'URL':url_list})

#This will print the above created dataframe
print(df)

#Creating an writer to create an excel file
writer = ExcelWriter('news_url_crawler.xlsx')

#entering the data from the dataframe to the excel file
df.to_excel(writer,'Sheet1', index = False)

#Saving the excel file
writer.save()
