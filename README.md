# Python Test
MAIN TASK
In this task we want you to scrape a minimum hundred URLs.The URL will be in format of "https://www.amazon.{country}/dp/{asin}".The country code and Asin parameters are in the CSV file https://docs.google.com/spreadsheets/d/1BZSPhk1LDrx8ytywMHWVpCqbm8URTxTJrIRkD7PnGTM/edit?usp=sharing. The CSV file contains 1000 rows.Use Selenium or bs4 to Scarpe the following details from the page.
1. Product Title
2. Product Image URL
3. Price of the Product
4. Product Details
If any URL throws Error 404 then print the {URL} not available and skip that URL.

SOLUTION
Technology Used : Python, SQL, GIT , Selenium

Approch To Solve : The main goal is to scrap 1000's amazon urls in minimal time period therefore i use multithreading using python and concurrent.futures. With this approch i can manage 20 threads at a time and in each thread i pass 20 urls batch\Chunks (By reading CSV file using file handling and load all data in data veriable, then this data is used for makeing 1000 URLs in given format) with the help of python genrator function i.e iterate_in_batches which takes alldata and no of bacth size to make small chunks. In thred function i.e open_chrome_browser this is main function which takes list of urls data in the form of chunks then i use selenium for open chrome and in for loop i itrate through all 20 urls and for handling exception i use try and except block . In try block i am scraping values of product_titles,product_image_urls,product_prices abd product_details and append to respected lists. after getting all imformations I convert all this data to json and write to data.json file and also insert data to SQL Lite database.

Result : It takes 25 mins for completeing all process for 1000 url data.
