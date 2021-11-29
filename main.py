import requests
from bs4 import BeautifulSoup
from selenium import webdriver

def main():
    driver = webdriver.Chrome()
    driver.get('https://www.facebook.com/profile.php?id=100011366594475')
    full_name = driver.find_element_by_tag_name("html")
    print(full_name.text)

if __name__ == "__main__":
    main()



#insert_resource(source_url, number_of_subscribers, first_name, second_name)
