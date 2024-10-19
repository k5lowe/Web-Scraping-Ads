import requests
from bs4 import BeautifulSoup
import json
import mysql.connector




#------------------  General Variables  ------------------#



# connect to database
db = mysql.connector.connect(
    host="host",                    # replace with your hostname
    user="user",                    # username
    password="password",            # password
    database="database"             # name of database
    )

cursor = db.cursor()

# general variables and queries
radius = 3.0
table = "ad_table"                  # replace with name of your table
check_query  = f"SELECT EXISTS(SELECT 1 FROM {table} WHERE `listing id` = %s)"
insert_query = f"INSERT INTO {table} (title,price,description,address,`listing id`) VALUES (%s,%s,%s,%s,%s)"
delete_query = f"DELETE FROM {table} WHERE `listing id` = %s"
listing_query= f"SELECT `listing id` FROM {table}"

# get all existing current listing ids from MySQL table
cursor.execute(listing_query)
table_listings = cursor.fetchall()
new_table_listings = set([lis[0] for lis in table_listings])



#====================  ALL FUNCTIONS  ====================#



def details(page_num,radius,total):
    """The details function inserts new data into a MySQL table and 
    deletes any rows where the listing ID is not present in the current 
    set of keys, ensuring that only up-to-date ads remain in the table."""

    try:

        ad_list_and_num = ad_page(page_num,radius)
        apollo = ad_list_and_num[0]                  # all the details of the main ads
        list_of_keys = ad_list_and_num[1]            # list of main ads
        limit = ad_list_and_num[2]                   # limit of ads per page
        total_count = ad_list_and_num[3]             # total number of ads across all pages
        num_of_ads = len(list_of_keys)               # number of ads on current page
        
        for key in list_of_keys:
            base = apollo[key]
            listing_id = int(base['id'])
            cursor.execute(check_query, (listing_id,))
            result = cursor.fetchone()

            if listing_id in new_table_listings:
                new_table_listings.discard(listing_id)

            if result[0] == 1:                       # if listing id is already in table go to next iteration
                continue

            title = base['title']
            price = "Please Contact"
            description = base['description']
            address = base['location']['address']
            # url = base['url']
        
            if base['price']['type'] == 'FIXED':
                price = f"${base['price']['amount'] / 100:.2f}"

            data = (title,price,description,address,listing_id)
            cursor.execute(insert_query,data)

        total += num_of_ads        

        if total == total_count:                     # delete any row/ad from table if not mentioned
            for key in new_table_listings:
                cursor.execute(delete_query, (key,))
            return None
        elif num_of_ads == limit:
            return details(page_num+1,radius,total)
    
    except (AttributeError,mysql.connector.Error):
        print("an error occurred")
        return None



def ad_page(page_num,radius):
    """ad_page extracts key information about an ad, including 
    its details, the listing IDs of the main ads (excluding top/
    featured ads to avoid duplication), the limit of ads displayed 
    per page, and the total number of ads across all pages."""

    ad_url = f"https://www.kijiji.ca/b-real-estate/kitchener-waterloo/rooms-for-rent/page-{page_num}/k0c34l1700212?address=University%20of%20Waterloo%2C%20University%20Avenue%20West%2C%20Waterloo%2C%20ON&ll=43.4722854%2C-80.5448576&radius={radius}"

    kijiji = requests.get(ad_url)
    kt = kijiji.text
    soup = BeautifulSoup(kt, 'lxml')
    body = soup.find("body")
    content = body.contents
    needed_content = content[2].text

    mydata = json.loads(needed_content)

    props = mydata.get("props", [])
    page_props = props.get("pageProps", [])
    apollo = page_props.get("__APOLLO_STATE__", [])
    root_query = apollo.get("ROOT_QUERY", [])

    part_of_url = find_main_listings_key(ad_url)
    search_results_key = next((key for key in root_query if part_of_url in key), None)
    
    search_results = root_query.get(search_results_key, [])
    pagination = search_results.get("pagination", [])
    limit = pagination.get("limit", [])
    total_count = pagination.get("totalCount", [])
    results = search_results.get("results", [])
    mainlisting = results.get("mainListings", [])

    list_of_keys = [i['__ref'] for i in mainlisting]
 
    return apollo,list_of_keys,limit,total_count



def find_main_listings_key(ad_url):
    """find_main_listings_key is designed to locate a specific 
    substring within a key that is too lengthy to use directly 
    in a get statement. By identifying the target substring, the 
    function helps store the complete, long key in a variable for 
    more efficient and readable access in subsequent operations"""

    new_url = ad_url.strip("https://www.kijiji.ca")
    address_index = new_url.index('address')
    part = new_url[:address_index]

    return part



details(page_num=1,radius=radius,total=0)

db.commit()
cursor.close()
db.close()