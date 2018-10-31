
# coding: utf-8

# In[1]:





# In[1]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import csv
import re
import time 
import pandas as pd 
driver = webdriver.Chrome()
destination_list = ['Lyon, France', 'Nice, France','Bordeaux,France','Marseille,France','Lille,France','Strasbourg,France','Nantes,France','Toulouse,France','Amsterdam,Pays-Bas','Genève, Suisse','Barcelona,Espagne']
csv_file=open('blabla.csv','w',encoding='utf-8')
writer=csv.writer(csv_file)

for dest in destination_list:
    driver.get("https://www.blablacar.fr/")
    from_box = driver.find_element_by_id("search_from_name")
    to_box = driver.find_element_by_id("search_to_name")
    from_box.send_keys('Paris, France')
    to_box.send_keys(dest)
    submit_button = driver.find_element_by_xpath('//button[@type="submit"]')
    submit_button.click()
    SCROLL_PAUSE_TIME = 2

    # Get scroll height
    last_height = driver.execute_script("return window.scrollY")
    count=0
    
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, window.scrollY+1000)")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return window.scrollY")
        if (new_height == last_height):
            break
        last_height = new_height
        count=count+1
            
    tag_List=driver.find_elements_by_xpath('//li[@itemtype="http://schema.org/Event"]')
    Link2=[]  
    d={}
    d['departure_time'] = []
    d['arrival_time'] = []
    for item in tag_List:
        try:
            time=item.find_element_by_xpath('.//ul[@class="jsx-4175336312 kirk-tripCard-itinerary"]')
            times = time.find_elements_by_xpath('.//time')
            departure_time=times[0].get_attribute("datetime")
            arrival_time=times[1].get_attribute("datetime")
        except:
            try:
                times = time.find_elements_by_tag_name('.//time')
                departure_time=times[0].get_attribute("datetime")
                arrival_time=times[1].get_attribute("datetime")
            except:
                times="NA"
                departure_time="NA"
                arrival_time="NA"
            
        d['departure_time'].append(departure_time)
        d['arrival_time'].append(arrival_time)
        
        
        
    # Data Frame containing departure time and arrival time
    Data=pd.DataFrame.from_dict(d)
           
        
    Link2.append(item.find_element_by_xpath('.//a').get_attribute("href")) 
           
    d1={} 
    d1['price']=[]
    d1['n_views']=[]
    d1['picture']=[]
    d1['n_places']=[]
    d1['driver_age']=[]
    d1['driver_name']=[]
    d1['Trip_Review']=[]
    d1['n_reviews']=[]
    d1['conduite']=[]
    d1['smoking']=[]
    d1['pets']=[]
    d1['email']=[]
    d1['telephone']=[]
    d1['n_facebook']=[]
    d1['n_annoucements']=[]
    d1['ID_verified']=[]
    d1['gender']=[]
    d1['seats']=[]
    

    
    for url in Link2: 

        driver.get(url)

        #scraping for price:
        try:
            price=driver.find_element_by_xpath('.//span[@class="u-right u-textBold u-darkGray size30 padding-right"]').text

        except:
            price="NA"
        print(price)
        d1['price'].append(price)

        # scraping for number of views and printed date
        try:
            #main_table=driver.find_element_by_xpath('.//div[@class="u-table"]')
            #main_table1=main_table.find_element_by_xpath('.//div[@class="u-cell u-alignRight u-alignTop"]')
            #main_table2=driver.find_element_by_xpath('.//div[RideDetails-publicationInfo u-table"]')
            n_views=driver.find_element_by_xpath('.//span[@class="u-cell"]').text
        except:
            n_views="NA"
        d1['n_views'].append(n_views)
        print(number_views)
        
        # scrap for picture tag
        try:
            picture0=driver.find_element_by_xpath('.//div[@class="ProfileCard-picture"]')
            picture1=picture0.find_element_by_xpath('.//img').get_attribute("src")
            b=picture1.find("avatar")
            if b!=-1:
                picture="picture not available"
            elif b==-1:
                picture="picture available"
            
        except:
            picture="NA"
        print(picture)    
        d1['picture'].append(picture)



            # scrap for number of remianing seats
        try:
            remaining_0=driver.find_element_by_xpath(('.//div[@class="Booking-occupancy Block-section"]'))
            remaining=remaining_0.find_element_by_xpath('.//div[@class="padding-top"]')
            remaining_places=remaining.find_element_by_xpath('.//span[@class="u-textBold u-darkGray size20"]').text

        except:
            remaining_places=0
        print(remaining_places)
        d1['n_places'].append(remaining_places)
           
            
            
            
            # scrap for total number of seats:
        try:
            seats0.find=driver.find_element_by_xpath('.//ul[@class="u-reset"]')
            seats1=seats0.find_elements_by_xpath('.//li[@class="Booking-occupant"]')
            seats=len(seats1)
        except:
            seats="NA"
        print(seats)
        d1['seats'].append(seats)
            

            # scrap for driver age & driver name
        try:
            block_age=driver.find_element_by_xpath('.//div[@class="ProfileCard-infosBlock"]')
            
            age=block_age.find_element_by_xpath('.//div[@class="ProfileCard-info"]').text
            block_name=driver.find_element_by_xpath('.//div[@class="ProfileCard-infosBlock"]')
            block_name1=block_name.find_element_by_xpath('.//h4[@class="ProfileCard-info ProfileCard-info--name u-truncate"]')
            name=block_name1.find_element_by_xpath('.//a[@rel="nofollow"]').text
        except:
            age="NA"
        print(name)
        print(age)
        d1['driver_age'].append(age)
        d1['driver_name'].append(name)

            # scrap for trip rating (numerical review)
        try:
            general_review=driver.find_element_by_xpath('.//p[@class="ratings-container"]')
            numerical_review=general_review.find_element_by_xpath('.//span[@class="u-textBold u-darkGray"]').text
            print(numerical_review)
        except:
            numerical_review="NA"
        print(numerical_review)
        d1['Trip_Review'].append(numerical_review)

            # scrap for trip rating (number of  review)
        try:
            general_review=driver.find_element_by_xpath('.//p[@class="ratings-container"]')
            number_of_reviews=general_review.find_element_by_xpath('.//span[@class="u-gray"]').text

        except:
            number_of_reviews="NA"
        print(number_of_reviews)
        d1['n_reviews'].append(number_of_reviews)



            #scrap driving rating 
        try:
            block_conduite=driver.find_element_by_xpath('.//div[@class="Block-section"]')
            profile=block_conduite.find_element_by_xpath('.//div[@class="ProfileCard"]')
            conduite=profile.find_element_by_xpath('.//div[@class="ProfileCard-row"][2]').text
        except:
            conduite="NA"
        d1['conduite'].append(conduite)
        print(conduite)


             #scrap for smoking permition
        try:
            regulations=driver.find_element_by_xpath('.//div[@class="ProfileCard-row u-clearfix"]')
            smoking=regulations.find_element_by_xpath('.//span[@class="no-smoking prefs tip"]').get_attribute("oldtitle")
            if smoking=="La cigarette me dérange.":
                smoking="smoking not allowed"
            if smoking=="La cigarette ne me dérange pas.":
                smoking=="smoking allowed"
        except:  
            smoking="smoking allowed"
        print(smoking)
        d1['smoking'].append(smoking)

            # scrap for pets acceptable 
        try:
            regulations=driver.find_element_by_xpath('.//div[@class="ProfileCard-row u-clearfix"]')
            pets=regulations.find_element_by_xpath('.//span[@class="no-pet prefs tip"]').get_attribute("oldtitle")
            if pets=="Je n'ai rien contre les animaux.":
                pets="pets allowed"
            if pets=="Je ne veux pas voyager avec un animal.":
                pets="pets not allowed"
        except:

            pets="pets allowed"

        d1['pets'].append(pets)
        print(pets)
        
        


        #scrap to check telephone verfication
        try:
            block_telephone=driver.find_element_by_xpath('.//div[@class="Block-section"]')
            element=block_telephone.find_element_by_xpath('//li[@class="main-column-list verification-list unstyled"]')
            telephone=element.find_element_by_xpath('//span[@class="u-alignMiddle u-green bold tip"]').get_attribute("oldtitle")
            if telephone=="Nous avons vérifié que le numéro de téléphone indiqué par ce membre permet bien de le joindre.":
                 telephone=" telephone available"
        except:
            telephone="telephone not available"
        print(telephone)
        d1['telephone'].append(telephone)




            #scrap to check email verification
        try:
            block_email=driver.find_element_by_xpath('.//div[@class="Block-section"]')
            element_1=block_email.find_element_by_xpath('.//li[@class="main-column-list verification-list unstyled"]')
            email_1= element_1.find_element_by_xpath('.//span[@class="u-alignMiddle u-green bold tip"]').get_attribure("oldtitle")
            
            if email_1=="Nous avons vérifié l'e-mail de ce membre.":
                email="email available"
        except:
            email="NA"
        print(email)
        d1['email'].append(email)

            # scrap number of facebook freinds for drivers
        try:
            block_1=driver.find_element_by_xpath('.//div[@class="Block-section"]')
            block_2=block_1.find_elment_by_xpath('.//ul[class="main-column-list verification-list unstyled"]')
            block_3=block_2.find_element_by_xpath('.//li')
            n_facebook=block_3.find_element_by_xpath('.//span[class="u-alignMiddle u-green bold"]').text
        except:
             n_facebook=0
        print(n_facebook)
        d1['n_facebook'].append(n_facebook)



            #scrap for number of annoucements
        try:
            n_annoucements0=driver.find_element_by_xpath('.//div[@class="Block-section"]')
            n_annoucements1=n_annoucements0.find_element_by_xpath('.//ul[@class="main-column-list u-reset"]')
            n_annoucements= n_annoucements1.find_element_by_xpath('.//li').text
        except:
            n_annoucements="NA"
        print( n_annoucements)
        
        d1['n_annoucements'].append(n_annoucements)
        
           #scrap identity card
            
        try:
            verification_1=driver.find_element_by_xpath('.//div[@class="ProfileCard-infosBlock"]')
            liscense=verification_1.find_element_by_xpath('.//div[@class="ProfileCard-info u-blue"]').text
            a=liscense.find("Pièce d'identité vérifiée")
            if (a!=-1):
                ID_verified=True
            elif (a==-1):
                 ID_verified=False
        except:
            ID_verified=False
        print(ID_verified)
        d1['ID_verified'].append(ID_verified)
            
        
           #scrap gender values:
        try:
            gender0=driver.find_element_by_xpath('.//th[@id="driver"]')
            gender1=gender0.find_element_by_xpath('.//svg[@title="Conducteur"]')
            gender2=gender1.find_element_by_xpath('.//use').get_attribute("xlink:href")
            c=gender2.find("m")
            d=gender2.find("f")
            if (c==-1):
                gender="female"
            if (c!=-1):
                gender="male"
        except:
            gender="not specified"
        print(gender)
        d1['gender'].append(gender)
    Data_1=pd.DataFrame.from_dict(d1)
    
    Bla_Bla=pd.concat([Data,Data_1])
    
  

   

    writer.writerow(d.values())

    
                                                 
                                                 
    
                                                 
        
            
        

           


# In[53]:


a="\n                                Pièce d'identité vérifiée\n                            "
print(a)


# In[54]:


a.find("Pièce d'identité vérifiée")


# In[55]:


"hello".find("Pièce d'identité vérifiée")


# In[77]:


a="#icon-avatar-driver-m"
a[-1]


# In[ ]:


seats0.find=driver.find_element_by_xpath('.//ul[@class="u-reset"]')
            seats1=seats0.find_elements_by_xpath('.//li[@class="Booking-occupant"]')
            seats=len(seats1)

