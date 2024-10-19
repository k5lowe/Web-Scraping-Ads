# Web-Scraping-Ads
Scrape ad details and store the relevant information in a MySQL table.

## Description ##
This project involves developing a Python-based web scraper to extract detailed information from online ads. The key features include identifying and collecting ad details, such as pricing, description, and listing IDs, while avoiding duplicate or featured ads. The scraped data is then inserted into a MySQL database, where it is efficiently managed.

The details function handles inserting new ad data into the MySQL table and ensures that outdated ads (ads no longer present in the scraped list) are deleted. This system is designed to keep the database up-to-date with the most current ad listings, providing an automated and optimized solution for managing ad data.

Features:
- Ad scraping (extract title, price, description, address, listing IDs)
- MySQL Database Integration
- Avoid duplicate and top/featured ads
- Delete outdated ads from MySQL table
- Check for existing ads before inserting
- Error Handling
- Batch Processing
- Concurrency-friendly database operations

Technologies:
- Python
- MySQL
- Beautiful Soup
- JSON

## Notes ##

The provided link (URL) example below does not follow the default format used by Kijiji. To obtain the correct format, navigate to a page that is not the first page, and copy the URL. The resulting URL should match the structure shown below, but without the formatted variable values. The original code is designed to work with URLs of a specific format, where the page number and radius are variables. To ensure the code functions correctly, any URL provided must adhere to this specified format.

### Complete Url ###
```python
f"https://www.kijiji.ca/b-real-estate/kitchener-waterloo/rooms-for-rent/page-{page_num}/k0c34l1700212?address=University%20of%20Waterloo%2C%20University%20Avenue%20West%2C%20Waterloo%2C%20ON&ll=43.4722854%2C-80.5448576&radius={radius}"
```
### Complete Formatted Url ###
```python
https://www.kijiji.ca/b-real-estate/kitchener-waterloo/rooms-for-rent/page-1/k0c34l1700212?address=University%20of%20Waterloo%2C%20University%20Avenue%20West%2C%20Waterloo%2C%20ON&ll=43.4722854%2C-80.5448576&radius=3
```
For example the first/third code should look like the second/fourth, respectively:

#### page_num: ####
```python
url = "...rent/page-1/k0c34..."
```
```python
url = "...rent/page-{page_num}/k0c34..."
```
#### radius: ####
```python
url = "...80.5448576&radius=3.0"
```
```python
url = "...80.5448576&radius={radius}"
```



## Attributions & Remarks ##

The entirity of this project rested on the kind help of the following websites. As always, ChatGPT proved an immense help and guidance where much time and effort was saved

- https://chatgpt.com/
- https://www.w3schools.com/
- https://medium.com/@kaineblack/web-scraping-kijiji-ads-with-python-ef81a49e0e9e
- https://www.youtube.com/watch?v=9ADd-_mM5Dw&ab_channel=ProgrammingKnowledge

Please feel free to use this code! Lastly, any feedback on how to optimize this code would be greatly appreciated. Thank you for your time.
