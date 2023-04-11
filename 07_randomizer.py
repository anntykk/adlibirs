
"""

MODULE: Randomizer
DESCRIPTION: Connects to database and selects random book based on filter(s)

"""

##############################################################################
###   CONNECT TO MYSQL   ######################################################

### Create connector
try:
    cnx = mysql.connector.connect(user=user, password=password,
                                  host=host,
                                  database=database) # Connects to MySQL server

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
###   SELECT FILTERS   #######################################################

# Selected filter for category
category = 'Skönlitteratur'

##############################################################################
###   QUERY DATA   ###########################################################

# Query to select a random book based on selected filters
query = ("SELECT books.isbn, books.title, books.rating "
         "FROM books "
         "LEFT JOIN books_categories ON books.isbn = books_categories.isbn "
         "WHERE books_categories.category = %s "
         "ORDER BY RAND() LIMIT 0,1")

cursor.execute(query, (category,))

# Obtain information on the random book
result = cursor.fetchall()

isbn = result[0][0]

book = result[0][1]

rating = result[0][2]

# Query to obtain information on author of that book
query = ("SELECT books.isbn, books_authors.author "
         "FROM books "
         "LEFT JOIN books_authors ON books.isbn = books_authors.isbn "
         "WHERE books.isbn = %s ")

cursor.execute(query, (isbn,))

result_authors = cursor.fetchall()

##############################################################################
###   RUN RANDOMIZER   #######################################################
print('Slumpgeneratorn föreslår bokklubben att läsa '
      + '\n####' + book + '####'
      + '\nsom har skrivits av ')
try: 
    for author in result_authors:
        print('####' + author[1] + '####')
except: print("####Författarnamn saknas####")
print('inom kategorin'
      '\n####' + category + '####')
if rating != None:
    print('och som har fått ' 
          + '\n####' + str(rating) + ' av 5 i betyg####')


