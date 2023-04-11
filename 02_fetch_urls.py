
"""

MODULE: Fetch urls
DESCRIPTION: Fetches urls to books landing page and saves to log-file

"""

##############################################################################
###   DEFINE URL   ###########################################################

# Build the url based on url_base and url_parameters
url_base = "https://www.adlibris.com/se/avdelning/skonlitteratur-7380"
url_parameters = ["id=7380",
                  "filter=format_sv%3apocket",
                  "filter=released%3aa",
                  "filter=grouped_language_sv:svenska",
                  "sort_by=published",
                  "order_by=desc",
                  "pn={page_nr}",
                  "ps=100"
                  ]
url_parameters = "&".join(url_parameters)
url = url_base + "?" + url_parameters

# Define maximum page number
page_nr = 1
page_nr_max = 12

# List the all urls to be fetched
urls_to_fetch = []

while page_nr <= page_nr_max:
    url_to_fetch = url.format(page_nr=str(page_nr))
    urls_to_fetch.append(url_to_fetch)
    page_nr += 1
    
# Save the urls to be fetched
file_name = "urls_to_fetch.txt"
path = log_urls_folder.joinpath(file_name)

with open(path,"w") as text_file:
	text_file.write("\n".join(urls_to_fetch))

##############################################################################
###   LIST REMAINING URLS TO BE FETCHED   ####################################

# Open list with urls to fetch
file_name = "urls_to_fetch.txt"
path = log_urls_folder.joinpath(file_name)

with open(path,"r") as text_file:
	urls_to_fetch = text_file.read().split("\n")

# Open list with urls previously fetched and compare with urls to fetch to obtain list on urls to fetch
file_name = "urls_fetched.txt"
path = log_urls_folder.joinpath(file_name)

if os.path.exists(path):
    with open(path,"r") as text_file:
    	urls_fetched = text_file.read().split("\n")
        
    urls_to_fetch = list(set(urls_to_fetch).difference(set(urls_fetched)))

else:
    urls_to_fetch = urls_to_fetch    

##############################################################################
###   FETCH URLS   ###########################################################

# Fetch links to book landing page 
url_dict = {}
urls_failed = []
urls_fetched = []

for url in urls_to_fetch:
    
    page = requests.get(url, timeout=30)
    
    if page.status_code != 200:
        urls_failed.append(url)
        print(f"Could not download url " + url)
        break
        
    soup = BeautifulSoup(page.text, "html.parser")
    results = soup.find_all("div", class_ = "item-info")
    
    # Fetch links to each book
    for item in results:
        item = item.find('a')['href']
        isbn_date = str(re.findall(r"[\d]{13}", item)[0]) + '_' + str(date.today()) # Use regex to extract ISBN and use as key
        url_dict[isbn_date] = item 
    
    urls_fetched.append(url)
    print(url + ' DONE!')

##############################################################################
###   SAVE TO FILE   #########################################################

# Save information about which URLs have been fetched
file_name = "urls_fetched.txt"
path = log_urls_folder.joinpath(file_name)

with open(path, "a") as text_file:
    text_file.write("\n".join(urls_fetched))

# Save information about links to book pages
timestamp = dt.datetime.now().strftime('%Y-%m-%dt%H-%M-%S')
file_name = f"urls_books_{timestamp}.json"
path = books_to_fetch_folder.joinpath(file_name)

with open(path, "w", encoding="utf-8") as json_file:
    json.dump(url_dict, json_file, ensure_ascii=False)











