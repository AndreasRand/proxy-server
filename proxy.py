import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from random import randint
import os


''' 
Function to read proxies from the website "https://hidemy.name/"
Returns the proxy list with proxies that were read from the website
'''
def site_read_loop(driver):
    proxy_list = []
    page_number = 1    # Counter for ouputting the current website
    list_size = 64    # Size for changing the URL to get new values, every URL has a table with the size 64
    while True:
        try:    # This wait is for the cloudfare check that occurs sometimes and should take less than 10 seconds, if not then there's some other issue
            table_body = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))    # Find the table body
        except:
            driver.quit()
            print("Error loading the proxy website")
            return
        table_rows = table_body.find_elements(By.TAG_NAME, "tr")    # Find all rows from the table
        if len(table_rows) == 0:    # There is no 404 error in case the current URL size is bigger the actual available proxies, so we are checking if the table is empty in that case
            break
        print("Page",str(page_number)+"...")
        for row in table_rows:
            columns = row.find_elements(By.TAG_NAME, "td")
            if int(columns[3].text.split(" ")[0]) < 1000:    # Only proxies with faster speeds than 1000 are chosen
                new_proxy = columns[0].text + ":" + columns[1].text
                proxy_list.append(new_proxy.strip("\n"))
        page_number += 1
        driver.get("https://hidemy.name/en/proxy-list/?type=s&start="+str(list_size)+"#list")    # Opens the next URL
        list_size += 64

    return proxy_list


# Function to write the new proxies to the file
def write_to_file(new_proxy_list):
    old_proxy_list = []
    file = open("proxy_list.txt")    # Open for reading
    for row in file:
        old_proxy_list.append(row.strip("\n"))    # Add all old proxies to a list
    file.close()
    file = open("proxy_list.txt", "a")    # Open for writing
    for proxy in new_proxy_list:
        if proxy not in old_proxy_list:    # If the new proxy is not already in the file then add it
            file.write(proxy+"\n")
    file.close()
    print("\nNew proxies are added to the file, run the program again to use them")


# This function prepares the driver for reading the proxies from the website and then writes them to the file
def proxy_list_creator():
    # This version of chromedriver (undetected chromedriver) has some initializing issues that are resolved with rerunning the driver
    for x in range(10):
        try:
            driver = uc.Chrome()
            break    # Break the loop if the driver is initialized
        except:
            pass
    driver.get("https://hidemy.name/en/proxy-list/?type=s#list")    # Open the URL with the type specified (s - secure/HTTPS)
    write_to_file(site_read_loop(driver))    # Write proxies to the file
    driver.quit()


''' 
Function to test the chosen proxy server, will load the website "https://whatismyipaddress.com/" to confirm that the proxy worked
If the page is not loaded it will be classified as a bad proxy and it will be removed from the file, after it's removed a new proxy will be chosen until one works
The two most common errors that occur when a bad proxy is found are "err_proxy_connection_failed" and "err_connection_closed" but all errors are checked
The request has a 5 second timeout period
'''
def test_proxy(driver, proxy_list, random_int):
    print("The new IPv4 address: " + proxy_list[random_int].strip("\n"))
    try:
        driver.get("https://whatismyipaddress.com/")    # Page to see if the IPv4 or IPv6 address has changed
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "ip-address-list")))    # Check if the page has loaded or not
        input("Exit?")    # Asking input to keep the driver running
        driver.quit()
    except:    # If the page didn't load
        driver.quit()
        print("A bad proxy was found, removing it and trying the next one..")
        proxy_list.remove(proxy_list[random_int])
        file = open("proxy_list.txt", "w")
        for proxy in proxy_list:    # Rewrite the new list without the bad proxy
            file.write(proxy)
        file.close()
        change_proxy()    # Call the proxy changing function again


# Function to run the chromedriver with the randomly chosen proxy server from the file
def change_proxy():
    proxy_list = []
    file = open("proxy_list.txt")
    for row in file:    # Read all proxies from the file
        proxy_list.append(row)
    file.close()
    if len(proxy_list) == 0:    # No proxies left in the file
        print("You have no proxies stored in the file!\n")
        get_input()
        return
    random_int = randint(0,len(proxy_list)-1)    # Random integer to choose a proxy from the list
    options = uc.ChromeOptions()
    options.add_argument('--proxy-server=' + proxy_list[random_int].strip("\n"))    # Add the proxy server to the options
    # This version of chromedriver (undetected chromedriver) has some initializing issues that are resolved with rerunning the driver
    for x in range(10):
        try:
            driver = uc.Chrome(options=options)
            break    # Break the loop if the driver is initialized
        except:
            pass
    
    test_proxy(driver, proxy_list, random_int)


''' 
Function to get the input from the user
This function has two possible outcomes based on the choice of the user
0 - a random proxy server will be chosen and used
1 - the proxy_list text file will be populated with new proxies if there are any new ones found
'''
def get_input():
    choice = int(input("Enter 0 if you want to use the proxy, enter 1 if you want to populate the file with new proxies: "))
    if choice == 0:
        if os.path.isfile('./proxy_list.txt'):    # Check if the proxy list file exists
            change_proxy()
        else:
            print("The required file for proxies does not exist in this path, so it will be created.")
            file = open("proxy_list.txt", "a")    # Create an empty file
            file.close()
            proxy_list_creator()
    elif choice == 1:
        print("Your proxy list will be updated..")
        proxy_list_creator()


get_input() # Call the main function
