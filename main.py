import csv
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.common.by import By
import sqlite3
import json
import time

def load_file():
    # Specify the path to your CSV file
    csv_file_path = 'C:/Users/SUMIT/Downloads/Amazon-Scraping-Sheet1.csv'  # Replace with your CSV file path

    # Initialize an empty list to store the data
    data = []
    # Open the CSV file in read mode
    with open(csv_file_path, mode='r', newline='') as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)    
        header = next(csv_reader, None)  
        
        for row in csv_reader:
            data.append(row)

    return data

# Iterate through the data in batches
def iterate_in_batches(alldata, batch_size):
    for i in range(0, len(alldata), batch_size):
        yield alldata[i:i + batch_size]

# Create lists to store the scraped data
product_titles = []
product_image_urls = []
product_prices = []
product_details = []
urls = []

# Function to open a Chrome browser instance
def open_chrome_browser(mydata):
    
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=chrome_options)
    for j in mydata:        
        # Open the first URL in the first tab
        url = f"https://www.amazon.{j[3]}/dp/{j[2]}"
        driver.get(url)
        try:
            title = driver.find_element(By.ID,"productTitle").get_attribute("value")
            product_titles.append(title)
            image_url = driver.find_element(By.ID,"productImageUrl").get_attribute("value")
            product_image_urls.append(image_url)
            prices = driver.find_element(By.ID,"priceValue").get_attribute("value")
            curr = driver.find_element(By.ID,"priceSymbol").get_attribute("value")
            product_prices.append(f'{prices} {curr}')
            details = driver.find_element(By.XPATH, "//div[@id='detailBullets_feature_div']").text
            product_details.append(details)
            urls.append(url)
            continue
        except Exception as e:
            print(f'URL - {url} not available')
            continue
            
            
            
    driver.quit()   
    

if __name__ == "__main__":
    # Number of Chrome browsers to open
    # Connect to an existing database or create a new one
    start_time = time.time()
    conn = sqlite3.connect('mydatabase.db')
    # Create a cursor
    cursor = conn.cursor()
    # Create a table (if it doesn't exist)
    cursor.execute('''CREATE TABLE IF NOT EXISTS product (
                        id INTEGER PRIMARY KEY,
                        url TEXT,
                        productIMGURL TEXT,
                        productTitle TEXT,
                        productPrice TEXT,
                        productDetails TEXT
                    )''')
    
    num_browsers = 20
    data  = load_file()
    # Create a thread pool with the desired number of threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_browsers) as executor:    
        browser_instances = {executor.submit(open_chrome_browser, batch) : batch for batch in iterate_in_batches(data, num_browsers)}      

    result = dict()        
    # Print the scraped data
    for i in range(len(product_titles)):
        result[urls[i]] = {"Product Title:" : product_titles[i],"Product Image URL:": product_image_urls[i],"Price of the Product:": product_prices[i],"Product Details:": product_details[i]}
                
        cursor.execute(f"INSERT INTO product (url,productIMGURL,productTitle,productPrice,productDetails) VALUES ('{urls[i]}','{product_image_urls[i]}','{product_titles[i]}','{product_prices[i]}','{product_details[i]}')")
    
    json_data = json.dumps(result)
    with open('data.json', 'w') as json_file:
        json_file.write(json_data)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    end_time = time.time()
    execution_time =  end_time - start_time
    print("Execution time:",execution_time)

