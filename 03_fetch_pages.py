
"""

MODULE: Fetch pages
DESCRIPTION: Uses selenium to open browser and save book pages to html-files

"""

##############################################################################
###   OPEN LINKS TO BOOKS FROM FILE   ########################################

file_list = list(glob.glob(str(books_to_fetch_folder) + '/*.json'))

url_dict = {} # Create empty dictionary
    
for file in file_list:
    with open(file, 'r') as f:
        temp = json.load(f) # Open saved dictionary with urls
        url_dict.update(temp)

##############################################################################
###   START UP SELENIUM   ####################################################

# Selenium start up webdriver
wd_path = os.path.join(home_folder, "chromedriver.exe").strip("/") 
service = ChromeService(executable_path=wd_path) #https://www.selenium.dev/documentation/webdriver/getting_started/upgrade_to_selenium_4/
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
driver = webdriver.Chrome(service=service, options=options) #https://www.selenium.dev/documentation/webdriver/getting_started/upgrade_to_selenium_4/

##############################################################################
###   SAVE TO FILE   #########################################################

# Fetch book page and save to file
for url_id, url in url_dict.items(): 
    time.sleep(randint(2,5)) #this is the time-out
    
    driver.get(f"https://www.adlibris.com{str(url)}") # Opens the browser

    page = driver.find_element(By.CLASS_NAME, "product-page__product-container").get_attribute("outerHTML") # Finds the part of the page to be saved 
    #print(page)

    file_name = "{}.html".format(url_id) # Creates a dynamic file name

    with open(os.path.join(books_to_parse_folder, file_name), 'w') as f:
        f.write(page) # Writes the page to a htlm-file
        
    print("URL " + str(url_id) + " IS DONE!") # Prints status

driver.quit() # Closes the browser

##############################################################################
###   MOVE DONE FILES   ######################################################

old_path = books_to_fetch_folder
new_path = books_to_parse_folder

for file in file_list:
    file_name = file.split("/")[-1]
    os.rename(old_path.joinpath(file_name), new_path.joinpath(file_name))
    











