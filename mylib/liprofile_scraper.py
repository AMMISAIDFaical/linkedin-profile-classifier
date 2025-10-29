import sys
print(sys.executable)
print(sys.version)
from bs4 import BeautifulSoup
import selenium
import selenium.webdriver as webdriver
import requests
from bs4 import BeautifulSoup

session = requests.Session()



# Set up Selenium WebDriver
driver = webdriver.Chrome()

# Go to LinkedIn's login page
driver.get("https://www.linkedin.com/login")

# Find the username and password fields
username = driver.find_element_by_name("session_key")
password = driver.find_element_by_name("session_password")

# Enter your credentials
username.send_keys("faical.ammisaid@outlook.com")
password.send_keys("$lumerican4l!fe")

# Log in using Selenium to retrieve cookies
for cookie in driver.get_cookies():
    session.cookies.set(cookie['name'], cookie['value'])
    
url = "https://linkedin.com/in/benmah"

# Make requests using the session
response = session.get(url)

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find the name element by inspecting LinkedIn's HTML structure
name = soup.find('h1', class_='text-heading-xlarge').get_text().strip()

# Find job title and company
job_title = soup.find('div', class_='text-body-medium').get_text().strip()
company = soup.find('span', class_='company-name').get_text().strip()

print(f"Name: {name}")
print(f"Job Title: {job_title}")
print(f"Company: {company}")