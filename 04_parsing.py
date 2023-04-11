
"""

MODULE: Parsing
DESCRIPTION: Parses the book pages to obtain information on books

"""

##############################################################################
###   OPEN LINKS TO BOOKS FROM FILE   ########################################
file_list = list(glob.glob(str(books_to_parse_folder) + '/*.json'))

url_dict = {} # Create empty dictionary
    
for file in file_list:
    with open(file, 'r') as f:
        temp = json.load(f) # Open saved dictionary with urls
        url_dict.update(temp)

##############################################################################
###   OPEN HTML BOOKS FROM FILE   ############################################

# Create empty dictionary
books_dict = {} 

# Define types of attributes to be parsed
tag_type_1_list = ["product__title__main-part",
                 "product__rating__amount"]

tag_type_2_list = ["product__stars__wrapper"]

# Loop through books
for url_id, url in url_dict.items():
        
    with open(os.path.join(books_to_parse_folder, url_id + ".html"), 'r') as f:
        soup = BeautifulSoup(f.read(), "html") # Opens the page html-file and creates a soup-object
        
    item_dict = {} # Create an empty dictionary to use within the loop

    # Parse product attributes
    for item in soup.find_all("div", class_ = "product__attribute"):
       key = item.find("span", class_ = "product__attribute__name").text #key
       try:
           value = list(item.find_all(class_ = "product__attribute__values")[0]) #value
       except:
           value = ""
       item_dict[key] = value

    for key in item_dict.keys():
       values = []
       for tag in item_dict[key]:
           values.append(tag.text)
       item_dict[key] = values
    
    item_dict["url"] = [url]

    # Parse type 1 attributes
    for tag in tag_type_1_list:
        try:
            item_dict[tag] = list(soup.find("span", class_ = tag))
        except:
            print(tag, " FAILED!!")
    
    # Parse type 2 attributes
    for tag in tag_type_2_list:
        try:
            item_dict[tag] = soup.find("div", class_ = tag).get("title")
        except:
            print(tag, " FAILED!!")
    
    # Parse category attributes
    try:
        soup_category = soup.find("ul", class_ = "product__link-list__list")
            
        category_list = []
            
        for category in soup_category.find_all('a', href=True):
            category_list.append(category.text)
            item_dict["category"] = category_list   
    except: 
        print("category FAILED")
        item_dict["category"] = []  


    books_dict[url_id] = item_dict # Appends the dictionary to dictionary books with url_id as key

    print("FILE " + str(url_id) + " DONE!")
    
##############################################################################
###   MOVE DONE FILES   ######################################################

# Move dict with book pages
old_path = books_to_parse_folder
new_path = old_path.joinpath("done")

for file in file_list:
    file_name = file.split("/")[-1]
    os.rename(old_path.joinpath(file_name), new_path.joinpath(file_name))
    
# Move html-files with books
book_list = list(glob.glob(str(books_to_parse_folder) + '/*.html'))

for book in book_list:
    file_name = book.split("/")[-1]
    os.rename(old_path.joinpath(file_name), new_path.joinpath(file_name))
    
    
    
    
    
    

    
 












    
    
    
    