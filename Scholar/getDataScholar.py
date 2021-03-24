# -*- coding: utf-8 -*-
# import build-in packages
import time
import os
from pandas.core.tools.datetimes import to_datetime
import pip
import warnings
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime







# ignore future warnings
warnings.filterwarnings("ignore")


# call for pip command
def install(package):
    pip.main(['install', package])


# pandas, bs4, selenium, webdriver-manager, ftfy packages
def requirements_check(package):
    try:
        __import__("pandas")
        __import__("bs4")
        __import__("selenium")
        __import__("webdriver_manager")
        __import__("ftfy")
        __import__("numpy")
    except:
        import sys
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', "pandas"])
        __import__("pandas")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', "bs4"])
        __import__("bs4")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', "selenium"])
        __import__("selenium")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', "webdriver-manager"])
        __import__("webdriver_manager")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', "ftfy"])
        __import__("ftfy")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', "numpy"])


requirements_check("pandas")
requirements_check("bs4")
requirements_check("selenium")
requirements_check("webdriver_manager")
requirements_check("ftfy")
requirements_check("numpy")

# Import packages
import pandas as pd
from selenium import webdriver
from bs4 import SoupStrainer
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from ftfy import fix_encoding
import numpy as np

from urllib.parse import urlparse
import urllib.request as urllib2
from django.core.files import File
from django.core.files.base import ContentFile
import io


from article.models import Article
from register.models import UserProfile
from django.contrib.auth.models import User

import random
import string

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def data_profile(link):
    
    list_of_link =[]
    list_of_name = []
    list_of_avatar = []
    list_of_Affiliation = []
    list_of_EmailForVerification = []
    
    # options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    # options.add_argument('window-size=1920x1080')
    # options.add_argument("disable-gpu")
    
    options = webdriver.ChromeOptions() 
    options.add_argument("start-maximized")
    # options.add_argument('disable-infobars')
    
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options,)
    # driver = webdriver.Edge(EdgeChromiumDriverManager().install())
    driver.get(str(link))
    # driver.execute_script("arguments[0].click();", WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='recaptcha-checkbox goog-inline-block recaptcha-checkbox-unchecked rc-anchor-checkbox']/div[@class='recaptcha-checkbox-checkmark']"))))

    while True:
        time.sleep(2)
    
        htmlSource = driver.page_source
        only_id = SoupStrainer(id="gsc_sa_ccl")
        soup = BeautifulSoup(htmlSource, "html.parser", parse_only=only_id)
        
        for tr in soup.findAll("div", {"class": "gsc_1usr"}):
            for name in tr.findAll("h3", {"class": "gs_ai_name"}):
                list_of_name.append(name.find("a").text)
                if 'https://scholar' in str(name.find("a",  attrs={"href": True}).get('href')):
                    list_of_link.append(str(name.find("a",  attrs={"href": True}).get('href')))
                else:
                    list_of_link.append('https://scholar.google.com'+str(name.find("a",  attrs={"href": True}).get('href')))
            for avatar in tr.findAll("span", {"class": "gs_rimg gs_pp_sm"}):
                if 'https://scholar' in str(avatar.find("img", attrs={"src": True}).get("src")):
                    avatarMediumImage = str(avatar.find("img", attrs={"src": True}).get("src"))
                    avatarMediumImage = avatarMediumImage.replace("small_photo","medium_photo")
                    print(avatarMediumImage)
                    list_of_avatar.append(avatarMediumImage)
                else:
                    avatarMediumImage = str(avatar.find("img", attrs={"src": True}).get("src"))
                    avatarMediumImage= avatarMediumImage.replace("small_photo","medium_photo")
                    list_of_avatar.append('https://scholar.googleusercontent.com' + avatarMediumImage)
            for affiliation in tr.findAll("div", {"class": "gs_ai_aff"}):
                list_of_Affiliation.append(affiliation.text)
            for email in tr.findAll("div", {"class": "gs_ai_eml"}):
                list_of_EmailForVerification.append(email.text)
                
        
        for index in range(0,len(list_of_link)):
            try:
                profile = UserProfile.objects.get(name=fix_encoding(list_of_name[index]),Affiliation =fix_encoding(list_of_Affiliation[index]),EmailForVerification = fix_encoding(list_of_EmailForVerification[index]), homepage = list_of_link[index])
            except:
                profile = None
            # print(profile)
            if profile == None and "FPT University" in list_of_Affiliation[index] :
                # print("Set data")
                user = User(username = get_random_string(12), password=get_random_string(8))
                user.save()
                profile = UserProfile(user = user ,name=fix_encoding(list_of_name[index]),Affiliation =fix_encoding(list_of_Affiliation[index]),EmailForVerification = fix_encoding(list_of_EmailForVerification[index]), homepage = list_of_link[index])
                img_url = list_of_avatar[index]
                name_image = urlparse(img_url).path.split('/')[-1]
                content = io.BytesIO(urllib2.urlopen(img_url).read())
                profile.avatar.save(name_image, content, save=True)
                profile.save()
        list_of_link =[]
        list_of_name = []
        list_of_avatar = []
        list_of_Affiliation = []
        list_of_EmailForVerification = []
                
        # show_more_button = driver.find_element_by_xpath('//button[@aria-label="Next"]')
        # while show_more_button.is_enabled() is not False:
        #     show_more_button.click()
        #     time.sleep(6)
        try:
            next_ = driver.find_element_by_xpath('//button[@aria-label="Next"]')
        except:
            next_ = None
        if next_ == None:
            break
        if next_.is_enabled() is not False:
            next_.click()
            time.sleep(6)
        else:
            break
            
    driver.close()
    # print(list_of_name)
    # print(list_of_link)
    # print(list_of_avatar)
    # print(list_of_Affiliation)
    # print(list_of_EmailForVerification)
    
    # # Create dataframe
    # df = pd.DataFrame(
    #     list(zip(list_of_name, list_of_Affiliation, list_of_EmailForVerification,list_of_avatar, list_of_link,)),
    #     columns=['name', 'Affiliation', 'EmailForVerification','avatar', 'homepage'])

    # # Fix unicode errors
    # df['name'] = df['name'].map(lambda x: fix_encoding(x))
    # df['Affiliation'] = df['Affiliation'].map(lambda x: fix_encoding(x))
    # df['EmailForVerification'] = df['EmailForVerification'].map(lambda x: fix_encoding(x))

    # # Output
    # df.to_csv('Profile-buff.csv', index=False)
    # file_name ='profile'+ datetime.now().strftime("%d-%m-%Y-%H-%M-%S") + ".csv"
    # df.to_csv(file_name, index=False)

    

def data_scrap(link,user):
    # Empty lists for storing information
    list_of_authors = []
    list_of_citation = []
    list_of_year = []
    list_of_articles = []
    list_of_journals = []
    list_of_conferences = []
    list_of_publication_date = []
    list_of_publisher = []
    list_of_pages = []
    list_of_volume = []
    list_of_issue = []
    list_of_book = []
    list_of_description = []
    list_of_pdf = []

    # Driver
    global driver
    # browser = ""
    # while browser != "exit":
    #     browser = input("Enter number of your browser: "
    #                     "\n1. Chrome"
    #                     "\n2. Edge"
    #                     "\n3. Firefox"
    #                     "\nYour choice: ")
    #     if browser == "1":
    #         driver = webdriver.Chrome(ChromeDriverManager().install())
    #         break
    #     elif browser == "2":
    #         driver = webdriver.Edge(EdgeChromiumDriverManager().install())
    #         break
    #     elif browser == "3":
    #         driver = webdriver.Firefox(GeckoDriverManager().install())
    #         break
    #     else:
    #         print("Valid value only in range 1->3")
    # options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    # options.add_argument('window-size=1920x1080')
    # options.add_argument("disable-gpu")
    
    options = webdriver.ChromeOptions() 
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(ChromeDriverManager().install(),  chrome_options=options)
    driver.get(str(link))
    time.sleep(1)

    # Locating the Show more button
    
    show_more_button = driver.find_element_by_xpath('//*[@id="gsc_bpf_more"]')

    while show_more_button.is_enabled() is not False:
        show_more_button.click()
        time.sleep(6)

    # Get author name, article name, year, total citation
    htmlSource = driver.page_source
    only_id = SoupStrainer(id="gsc_a_b")
    author_id = SoupStrainer(id="gsc_prf_in")
    soup = BeautifulSoup(htmlSource, "html.parser", parse_only=only_id)
    soup1 = BeautifulSoup(htmlSource, "html.parser", parse_only=author_id)
    author_name = soup1.find("div", {"id": "gsc_prf_in"})
    print("Author: " + author_name.text)
    for tr in soup.findAll("tr", {"class": "gsc_a_tr"}):
        for citation in tr.findAll("a", {"class": "gsc_a_ac gs_ibl"}):
            list_of_citation.append(citation.text)
        for year in tr.findAll("span", {"class": "gsc_a_h gsc_a_hc gs_ibl"}):
            list_of_year.append(year.text)
        for article in tr.findAll("a", {"class": "gsc_a_at"}):
            list_of_articles.append(article.text)

    # Set rational sleep time
    time.sleep(2)

    # Get everything u need
    clicks_on_article = driver.find_elements_by_class_name("gsc_a_at")
    clicks_on_X_button = driver.find_elements_by_id("gs_md_cita-d-x")

    index = 0
    
    for button in clicks_on_article:
        button.click()
        time.sleep(2)

        htmlSource = driver.page_source
        only_tags_with_id = SoupStrainer(id="gsc_vcd_table")
        soup = BeautifulSoup(htmlSource, "html.parser", parse_only=only_tags_with_id)
        for div in soup.findAll("div", {"class": "gsc_vcd_value"})[0]:
            list_of_authors.append(div)

        link_of_pdf = SoupStrainer(id="gsc_vcd_title_wrapper")
        soup_link = BeautifulSoup(htmlSource, "html.parser", parse_only=link_of_pdf)
        try:
            pdf_click = soup_link.find("a", attrs={"href": True})
            list_of_pdf.append(str(pdf_click.get('href')))
        except AttributeError:
            pdf_click = ""
            list_of_pdf.append(pdf_click)
        try:
            journal = soup.find(text="Journal").find_next().text
            list_of_journals.append(journal)
        except AttributeError:
            journal = ""
            list_of_journals.append(journal)
        try:
            conference = soup.find(text="Conference").find_next().text
            list_of_conferences.append(conference)
        except AttributeError:
            conference = ""
            list_of_conferences.append(conference)
        try:
            publication_date = soup.find(text="Publication date").find_next().text
            list_of_publication_date.append(publication_date)
        except AttributeError:
            publication_date = ""
            list_of_publication_date.append(publication_date)
        try:
            publisher = soup.find(text="Publisher").find_next().text
            list_of_publisher.append(publisher)
        except AttributeError:
            publisher = ""
            list_of_publisher.append(publisher)
        try:
            page = soup.find(text="Pages").find_next().text
            list_of_pages.append(page)
        except AttributeError:
            page = ""
            list_of_pages.append(page)
        try:
            volume = soup.find(text="Volume").find_next().text
            list_of_volume.append(volume)
        except AttributeError:
            volume = 0
            list_of_volume.append(volume)
        try:
            issue = soup.find(text="Issue").find_next().text
            list_of_issue.append(issue)
        except AttributeError:
            issue = ""
            list_of_issue.append(issue)
        try:
            book = soup.find(text="Book").find_next().text
            list_of_book.append(book)
        except AttributeError:
            book = ""
            list_of_book.append(book)
        try:
            description = soup.find(text="Description").find_next().text
            list_of_description.append(description)
        except AttributeError:
            description = ""
            list_of_description.append(description)
            
        if publication_date == "":
            Time=None
        else:
            # Time = to_datetime(str(publication_date), errors='coerce',yearfirst=True).date()
            Time = str(publication_date).replace('/','-');
            # Time = str(publication_date)[:4]
        print(Time)
        if volume==0:
            volume==None
        
        getyear = list_of_year[index]
        if getyear == "":
            getyear=None
        totle_citation = list_of_citation[index]
        if totle_citation=="":
           totle_citation=None 
        try:
            newarticle = Article.objects.get(user = user, 
                             title = fix_encoding(list_of_articles[index]), 
                             author=fix_encoding(list_of_authors[index]), 
                             total_citations=list_of_citation[index],
                             year=getyear,
                             url=list_of_pdf[index],)
        except:
            newarticle=None
        print(newarticle)
        if newarticle==None:
            newarticle = Article(user = user, 
                             title = fix_encoding(list_of_articles[index]), 
                             author=fix_encoding(list_of_authors[index]), 
                             publication_date= Time,
                             journal=fix_encoding(journal),
                             book=fix_encoding(book),
                             volume=volume,
                             issue= fix_encoding(issue),
                             conference=fix_encoding(conference),
                             page=page,
                             publisher=fix_encoding(publisher),
                             description=fix_encoding(description),
                             total_citations=totle_citation,
                             year=getyear,
                             url=list_of_pdf[index],)
            newarticle.save()
            print(newarticle)
        index+=1
        for button1 in clicks_on_X_button:
            button1.click()
        
    driver.close()
    '''
    for x in range(0, len(list_of_articles)):
        print(list_of_articles)

    # Create dataframe
    df = pd.DataFrame(
        list(zip(list_of_articles, list_of_authors, list_of_publication_date, list_of_book,
                 list_of_journals, list_of_volume, list_of_issue, list_of_conferences, list_of_pages, list_of_publisher, list_of_description, list_of_citation, list_of_year, list_of_pdf)),
        columns=['Article', 'Author', 'Publication date', 'Book', 'Journal',
                 'Volume', 'Issue', 'Conference', 'Page', 'Publisher', 'Description', 'Total citations', 'Year', 'Url'])

    # Fix unicode errors
    df['Article'] = df['Article'].map(lambda x: fix_encoding(x))
    df['Conference'] = df['Conference'].map(lambda x: fix_encoding(x))
    df['Journal'] = df['Journal'].map(lambda x: fix_encoding(x))
    df['Publication date'] = pd.to_datetime(df['Publication date'], errors='coerce')

    # Output
    df.to_csv('Citation_latest.csv', index=False)
    file_name = author_name.text + ".csv"
    df.to_csv(file_name, index=False)
    print("-----------------------------------------------")
    print("Your file is ready! Check " + str(file_name))
    print("-----------------------------------------------")
    print("PROCESS ENDED.")
    # input("Press Enter to continue...")
    '''
    print("-----------------------------------------------")
    print("Your file is ready! Check " + author_name.text)
    print("-----------------------------------------------")
    print("PROCESS ENDED.")


def time_ascending(name):
    file_valid = os.path.isfile(name)
    if file_valid:
        df = pd.read_csv(name)
        df.sort_values(by=['Year'], inplace=True)

        df = df.fillna(0)
        df['Year'] = df['Year'].astype('Int64').replace(0, np.nan)
        df['Total citations'] = df['Total citations'].astype('Int64').replace(0, np.nan)
        file_name_output = "TimeAscending " + name
        df.to_csv(file_name_output, index=False)
        print("-----------------------------------------------")
        print("Your file is ready! Check " + "\"" + file_name_output + "\"" + " !")
        print("-----------------------------------------------")
        input("Press Enter to continue...")
    else:
        print("File missing! Return to the Build Data step!")


def time_descending(name):
    file_valid = os.path.isfile(name)
    if file_valid:
        df = pd.read_csv(name)
        df.sort_values(by=['Year'], inplace=True, ascending=False)

        df = df.fillna(0)
        df['Year'] = df['Year'].astype('Int64').replace(0, np.nan)
        df['Total citations'] = df['Total citations'].astype('Int64').replace(0, np.nan)
        file_name_output = "TimeDescending " + name
        df.to_csv(file_name_output, index=False)
        print("-----------------------------------------------")
        print("Your file is ready! Check " + "\"" + file_name_output + "\"" + " !")
        print("-----------------------------------------------")
        input("Press Enter to continue...")
    else:
        print("File missing! Return to the Build Data step!")


def total_citations_ascending(name):
    file_valid = os.path.isfile(name)
    if file_valid:
        df = pd.read_csv(name)
        df.sort_values(by=['Total citations'], inplace=True)

        df = df.fillna(0)
        df['Year'] = df['Year'].astype('Int64').replace(0, np.nan)
        df['Total citations'] = df['Total citations'].astype('Int64').replace(0, np.nan)
        file_name_output = "TotalAscending " + name
        df.to_csv(file_name_output, index=False)
        print("-----------------------------------------------")
        print("Your file is ready! Check " + "\"" + file_name_output + "\"" + " !")
        print("-----------------------------------------------")
        input("Press Enter to continue...")
    else:
        print("File missing! Return to the Build Data step!")


def total_citations_descending(name):
    file_valid = os.path.isfile(name)
    if file_valid:
        df = pd.read_csv(name)
        df.sort_values(by=['Total citations'], inplace=True, ascending=False)

        df = df.fillna(0)
        df['Year'] = df['Year'].astype('Int64').replace(0, np.nan)
        df['Total citations'] = df['Total citations'].astype('Int64').replace(0, np.nan)
        file_name_output = "TotalDescending " + name
        df.to_csv(file_name_output, index=False)
        print("-----------------------------------------------")
        print("Your file is ready! Check " + "\"" + file_name_output + "\"" + " !")
        print("-----------------------------------------------")
        input("Press Enter to continue...")
    else:
        print("File missing! Return to the Build Data step!")


def sum_of_citations(name):
    file_valid = os.path.isfile(name)
    if file_valid:
        df = pd.read_csv(name)
        df = df.fillna(0)
        df['Total_citations'] = df['Total citations']
        df['Total_citations'] = df['Total_citations'].astype('Int64').replace(np.nan, 0)
        Total = df['Total_citations'].sum()
        print("-----------------------------------------------")
        print("Sum of Citation: " + str(Total))
        print("-----------------------------------------------")

        year = input("Enter year: ")

        print("Total citations in this year: " + str(df.loc[df['Year'] == int(year)].Total_citations.sum()))
        print("-----------------------------------------------")

        input("Press Enter to continue...")
    else:
        print("File missing! Return to the Build Data step!")


def filter_by_year(name):
    file_valid = os.path.isfile(name)
    if file_valid:
        year = input("Enter year: ")
        df = pd.read_csv(name)
        df1 = df.loc[df['Year'] == int(year)]
        is_empty = df1.empty
        while is_empty:
            print("This year is not found! Try again!")
            year = input("Enter year: ")
            df1 = df.loc[df['Year'] == int(year)]
            is_empty = df1.empty
            if is_empty is False:
                break
        file_name_output = "ArticleByYear " + name
        df.to_csv(file_name_output, index=False)
        print("-----------------------------------------------")
        print("Your file is ready! Check " + "\"" + file_name_output + "\"" + " !")
        print("-----------------------------------------------")
        input("Press Enter to continue...")
    else:
        print("File missing! Return to the Build Data step!")


def filter_by_number_of_citations_greater(name):
    file_valid = os.path.isfile(name)
    if file_valid:
        print("Will result years with total citations greater than the given value.")
        df = pd.read_csv(name)
        df1 = df.loc[df['Total citations'] >= int(number)]
        file_name_output = "NumberOfCitationsGreater " + name
        df1.to_csv(file_name_output, index=False)
        print("-----------------------------------------------")
        print("Your file is ready! Check " + "\"" + file_name_output + "\"" + " !")
        print("-----------------------------------------------")
        input("Press Enter to continue...")
    else:
        print("File missing! Return to the Build Data step!")


def filter_by_number_of_citations_less(name):
    file_valid = os.path.isfile(name)
    if file_valid:
        print("Will result years with total citations less than the given value.")
        df = pd.read_csv(name)
        df1 = df.loc[df['Total citations'] <= int(number)]
        file_name_output = "NumberOfCitationLess " + name
        df1.to_csv(file_name_output, index=False)
        print("-----------------------------------------------")
        print("Your file is ready! Check " + "\"" + file_name_output + "\"" + " !")
        print("-----------------------------------------------")
        input("Press Enter to continue...")
    else:
        print("File missing! Return to the Build Data step!")


value = '0'

# while value != "exit":
#     value = input("------------------------------------------------"
#                   "\nEnter one of the following values:"
#                   "\n0. Build data"
#                   "\n1. Arrange data (Time, Ascending)"
#                   "\n2. Arrange data (Time, Descending)"
#                   "\n3. Arrange data (Total citations, Ascending)"
#                   "\n4. Arrange data (Total citations, Descending)"
#                   "\n5. Citations (Sum)"
#                   "\n6. Filter articles by year"
#                   "\n7. Filter articles (condition)"
#                   "\n8. Quit"
#                   "\n-----------------------------------------------"
#                   "\nYour value: ")
#     if value == '0':
#         link = input("Enter the Scholar link: ")
#         while link == "":
#             link = input("This field must not be empty: ")
#         data_scrap(link)
#     if value == '1':
#         while True:
#             print()
#             a = input("Values: \n1. Start sorting (Time, Ascending)\n2. Return\nYour choice: ")
#             print()
#             if a == "1":
#                 name = input("Enter file name you want to work with: ")
#                 time_ascending(name)
#             elif a == "2":
#                 break
#     elif value == '2':
#         while True:
#             print()
#             a = input("Values: \n1. Start sorting (Time, Descending)\n2. Return\nYour choice: ")
#             print()
#             if a == "1":
#                 name = input("Enter file name you want to work with: ")
#                 time_descending(name)
#             elif a == "2":
#                 break
#     elif value == '3':
#         while True:
#             print()
#             a = input("Values: \n1. Start sorting (Total citations, Ascending)\n2. Return\nYour choice: ")
#             print()
#             if a == "1":
#                 name = input("Enter file name you want to work with: ")
#                 total_citations_ascending(name)
#             elif a == "2":
#                 break
#     elif value == '4':
#         while True:
#             print()
#             a = input("Values: \n1. Start sorting (Total citations, Descending)\n2. Return\nYour choice: ")
#             print()
#             if a == "1":
#                 name = input("Enter file name you want to work with: ")
#                 total_citations_descending(name)
#             elif a == "2":
#                 break
#     elif value == '5':
#         while True:
#             name = input("Enter file name you want to work with: ")
#             sum_of_citations(name)
#             break
#     elif value == '6':
#         while True:
#             name = input("Enter file name you want to work with: ")
#             filter_by_year(name)
#             break
#     elif value == '7':
#         while True:
#             print()
#             number = input("Enter number of citations: ")
#             a = input("Values: \n1. Greater than given value\n2. Less than given value\n3. Back\nYour value: ")
#             print()
#             if a == "1":
#                 name = input("Enter file name you want to work with: ")
#                 filter_by_number_of_citations_greater(name)
#                 break
#             elif a == "2":
#                 name = input("Enter file name you want to work with: ")
#                 filter_by_number_of_citations_less(name)
#                 break
#             elif a == "3":
#                 break
#     elif value == '8':
#         print("Program was terminated")
#         break
#     else:
#         print("Valid values are in range (0-->9) only!")
#         print()
