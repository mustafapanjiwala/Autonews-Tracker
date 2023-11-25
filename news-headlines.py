from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime
import os 
import sys
import pyodbc

# application_path = os.path.dirname(sys.executable)

now =datetime.now().strftime("%d-%m-%Y") #DDMMYYYY



website = "https://www.thesun.co.uk/sports/football/"

# Headless-mode


options = webdriver.ChromeOptions()
options.add_experimental_option('detach',True)
options.add_experimental_option('excludeSwitches',['enable-logging'])
# options.add_argument('--headless')


driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get(website)
driver.implicitly_wait(5)

# Get the headlines
container = driver.find_elements(by="xpath",value="//div[@class='teaser__copy-container']")

titles=[]
subtitles=[]
links=[]


for container in container:
    headline = container.find_element(by="xpath",value="./a/h2").text
    subtitle = container.find_element(by="xpath",value="./a/p").text
    link = container.find_element(by="xpath",value="./a").get_attribute("href")
    # headlines = driver.find_element(By.XPATH,"//div[@class='teaser__copy-container']/a/h2/text()")
    titles.append(headline)
    subtitles.append(subtitle)
    links.append(link)




myDict = {"Headlines":titles,"Subtitles":subtitles,"Links":links}
df= pd.DataFrame(myDict)
newpath = r'D:\Python Samples\News Automation\scraped_data' 
file_name = newpath+r"\News-headlines-"+now+r".csv"

if not os.path.exists(newpath):
    os.makedirs(newpath)

if os.path.exists(file_name):
    print(f"File {file_name} already exists. Choose a different name or delete the existing file.")
else:
    df.to_csv(file_name, index=False)
    print(f"Data saved to {file_name}")

driver.quit()

# Connecting to MySQL database

pyodbc.drivers()

conn = pyodbc.connect(Trusted_Connection='yes',driver='{ODBC Driver 17 for SQL Server}',server=r'MUSTAFA-PC\SQLEXPRESS',database='news_headlines')
cursor = conn.cursor()

cursor.execute("CREATE TABLE news_headlines (Headlines varchar(255), Subtitles varchar(255), Links varchar(255))")

df = pd.read_csv(file_name)
df = df.where(pd.notnull(df), None)

for row in df.itertuples():
    cursor.execute('''INSERT INTO news_headlines VALUES (?,?,?)''', row.Headlines, row.Subtitles, row.Links)

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

print(rf"Data exported to SQL Server 'MUSTAFA-PC\SQLEXPRESS' in database 'news_headlines', table 'news_headlines'.")
