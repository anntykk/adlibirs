
"""

MODULE: Cleaning
DESCRIPTION: Cleanes the data

"""

##############################################################################
###   CHANGE DATA TYPES   ####################################################

# Define attribute types
attribute_types = {'Författare: ':'list',
                   'Formgivare: ':'list',
                   'Fotograf: ':'list',
                   'ISBN: ':'string',
                   'Språk: ':'string',
                   'Vikt: ':'string',
                   'Utgiven: ':'string',
                   'Förlag: ':'string',
                   'Antal sidor: ':'string',
                   'url':'string',
                   'product__title__main-part':'string',
                   'product__rating__amount':'string',
                   'product__stars__wrapper':'string',
                   'Serie: ':'string',
                   'Upplaga: ':'string',
                   'Illustratör: ':'string',
                   'Översättare: ':'string',
                   'Redaktör: ':'list',
                   'Undertitel: ':'string',
                   'Ålder: ':'string',
                   'category':'list'} # Define attribute types in dictionary

# Create empty list to store potential attribute types that are missing in list
attribute_types_missing = [] 

# Loop through books and book attributes to change attribute type from list to string
for book in books_dict.keys():
    for attribute in books_dict[book].keys():
        if attribute in attribute_types.keys():
            attribute_type = attribute_types[attribute]
            if attribute_type == "list":
                 if type(books_dict[book][attribute]) != list:
                     books_dict[book][attribute] = [books_dict[book][attribute]]
            elif attribute_type == "string":
                 if type(books_dict[book][attribute]) == list:
                     books_dict[book][attribute] = books_dict[book][attribute][0]
                     if type(books_dict[book][attribute]) != str:
                         #print(f"Attribute {attribute} for book {book} should be string!!")
                         books_dict[book][attribute] = str(books_dict[book][attribute])
        else:
            attribute_types_missing.append(attribute) 

# Warn if not all attributes have their type defined
if len(attribute_types_missing) > 0:
    attribute_types_missing = list(set(attribute_types_missing))
    print("Some attributes do not have their type defined!") 

##############################################################################
###   SPLIT DATA   ###########################################################

# Obtain rating value
def clean_rating(item):
    try: 
        item = float(item.split(" ")[1])
    except: pass
    return item

for book in books_dict.keys():
    try:
        books_dict[book]['rating'] = clean_rating(books_dict[book]['product__stars__wrapper'])
    except: pass

# Obtain rating value and rating amount
def clean_count(item):
    try:
        item = int(item.split("\xa0")[0])
    except: pass
    return item

for book in books_dict.keys():
    try:
        books_dict[book]['RatingCount'] = clean_count(books_dict[book]['product__rating__amount'])
    except: pass

# Obtain publishing year
def clean_publ_year(item):
    try: 
        item = int(item.split("-")[0])
    except: pass
    return item

for book in books_dict.keys():
    try:
        books_dict[book]['Utgiven år: '] = clean_publ_year(books_dict[book]['Utgiven: '])
    except: pass





