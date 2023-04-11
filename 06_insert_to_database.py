
"""

MODULE: Insert to database
DESCRIPTION: Models the data and inserts to database

"""

##############################################################################
###   CONNECT TO MYSQL   ######################################################

### Create connector
try:
    cnx = mysql.connector.connect(user=user, password=password,
                                  host=host,
                                  database=database)

except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)

# Create cursor
cursor = cnx.cursor()

##############################################################################
###   INSERT DATA   ##########################################################

##############################################################################
### Insert books

# List attributes to include
attribute_list = ['ISBN: ',
                  'Antal sidor: ',
                  'Språk: ',
                  'Utgiven år: ',
                  'product__title__main-part',
                  'rating',
                  'RatingCount']

# Define script to insert data
add_book = ("INSERT INTO books "
            "(isbn,pages,language,pubYear,title,rating,ratingCount) " 
            "VALUES (%(ISBN: )s, %(Antal sidor: )s, %(Språk: )s, %(Utgiven år: )s, %(product__title__main-part)s, %(rating)s, %(RatingCount)s)")

# Create empty error list
book_error_list = []

# Loop through books_dict, for each book make sure that only and all the relevant attributes are included, insert to database
for book, attribute_dict in books_dict.items():
    book = dict(attribute_dict.items())
    for attribute in book.copy().keys(): # Loop through list of attributes to insert to database, delete attributes which are not in list
        if attribute in attribute_list:
            pass
        else:
            del book[attribute]
    for attribute_import in attribute_list: # Loop through attributes in book, if attribute is not in list, add it
        if attribute_import not in book.copy().keys():
            book[attribute_import] = None
        else:
            pass
    try:       
        cursor.execute(add_book, book) 
    except mysql.connector.IntegrityError as err:
        print("Error: {}".format(err)) # Try to import new rows, except if there are duplicates in isbn
        book_error_list.append("Error: {}".format(err))
        
# Export error list
with open(os.path.join(log_errors_folder, 'import_book_error_list' + str(date.today()) +'.json'), 'w') as f:
    json.dump(book_error_list, f, ensure_ascii=False) # Save dicionary to file

##############################################################################
### Insert authors

# List attributes to include
attribute_list = ['ISBN: ',
                  'Författare: ']

# Define script to insert data
add_author = ("INSERT INTO authors "
            "(author) "
            "VALUES (%(Författare: )s)")

add_book_author = ("INSERT INTO books_authors "
            "(isbn, author) "
            "VALUES (%(ISBN: )s, %(Författare: )s)")

# Create empty error list
author_error_list = []

book_author_error_list = []

# Loop through books_dict, for each book make sure that only and all the relevant attributes are included, insert to database
for book, attribute_dict in books_dict.items():
    book = dict(attribute_dict.items())
    for attribute in book.copy().keys(): # Loop through list of attributes to insert to database, delete attributes which are not in list
        if attribute in attribute_list:
            pass
        else:
            del book[attribute]
    for attribute_import in attribute_list: # Loop through attributes in book, if attribute is not in list, add it
        if attribute_import not in book.copy().keys():
            book[attribute_import] = None
        else:
            pass
    if type(book['Författare: ']) == list: # If-clause which only inserts data if there are values in the primary key field
        for author in range(len(book['Författare: '])): # Loop through authors in author-list. Create dictionary per book and author to insert to database
            book_author = {} # Create empty dictionary
            book_author['Författare: '] = book['Författare: '][author]
            book_author['ISBN: '] = book['ISBN: ']
            
            try:
                cursor.execute(add_author, book_author) # Insert author to database
            except mysql.connector.IntegrityError as err:
                author_error_list.append("Error: {}".format(err))
                
            try: 
                cursor.execute(add_book_author, book_author)# Insert book_author to database
            except mysql.connector.IntegrityError as err:
                book_author_error_list.append("Error: {}".format(err))
    else:
        print(book)
            
# Export error list
with open(os.path.join(log_errors_folder, 'import_author_error_list' + str(date.today()) +'.json'), 'w') as f:
    json.dump(author_error_list, f, ensure_ascii=False) # Save dicionary to file

with open(os.path.join(log_errors_folder, 'import_book_author_error_list' + str(date.today()) +'.json'), 'w') as f:
    json.dump(book_author_error_list, f, ensure_ascii=False) # Save dicionary to file


##############################################################################
### Insert categories

# List attributes to include
attribute_list = ['ISBN: ',
                  'category']

# Define script to insert data
add_category = ("INSERT INTO categories "
            "(category) "
            "VALUES (%(category)s)")

add_book_category = ("INSERT INTO books_categories "
            "(isbn, category) "
            "VALUES (%(ISBN: )s, %(category)s)")

# Create empty error list
category_error_list = []

book_category_error_list = []

# Loop through books_dict, for each book make sure that only and all the relevant attributes are included, insert to database
for book, attribute_dict in books_dict.items():
    book = dict(attribute_dict.items())
    for attribute in book.copy().keys(): # Loop through list of attributes to insert to database, delete attributes which are not in list
        if attribute in attribute_list:
            pass
        else:
            del book[attribute]
    for attribute_import in attribute_list: # Loop through attributes in book, if attribute is not in list, add it
        if attribute_import not in book.copy().keys():
            book[attribute_import] = None
        else:
            pass
    if type(book['category']) == list: # If-clause which only inserts data if there are values in the primary key field
        for category in range(len(book['category'])): # Loop through authors in category-list. Create dictionary per book and category to insert to database
            book_category = {} # Create empty dictionary
            book_category['category'] = book['category'][category]
            book_category['ISBN: '] = book['ISBN: ']
            
            try:
                cursor.execute(add_category, book_category) # Insert author to database
            except mysql.connector.IntegrityError as err:
                category_error_list.append("Error: {}".format(err))
                
            try: 
                cursor.execute(add_book_category, book_category)# Insert book_author to database
            except mysql.connector.IntegrityError as err:
                book_category_error_list.append("Error: {}".format(err))
    else:
        print(book)
            
# Export error list
with open(os.path.join(log_errors_folder, 'import_author_error_list' + str(date.today()) +'.json'), 'w') as f:
    json.dump(author_error_list, f, ensure_ascii=False) # Save dicionary to file

with open(os.path.join(log_errors_folder, 'import_book_author_error_list' + str(date.today()) +'.json'), 'w') as f:
    json.dump(book_author_error_list, f, ensure_ascii=False) # Save dicionary to file

##############################################################################
###  COMMIT AND DISCONECT FROM MYSQL   #######################################

cnx.commit() # Make sure data is committed to the database

cursor.close() # Close the cursor

cnx.close() # Close connector




