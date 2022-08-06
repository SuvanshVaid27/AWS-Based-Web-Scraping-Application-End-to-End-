# -----------------------------------------------------------
# This script extract headlines from google news with the search parameters as the top 10 cryptocurrencies
# and stores them into a table in the postgres database in the EC2 instance
#
# (C) Suvansh Vaid
# -----------------------------------------------------------

#!pip install beautifulsoup4
#!pip install sqlalchemy psycopg2
#!pip install python-dotenv

# Import required libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Top 10 popular crypto current topics 
topics = ['bitcoin', 'etherium', 'tether', 'USD Coin', 'binance', 'xrp', 'cardano', 'solana', 'dogecoin']

# Function to extract the news headlines from google news based on a topic
def extract(topic):

    # Google news search query 
    url = 'https://news.google.com/search?q={}&hl=en-AU&gl=AU&ceid=AU%3Aen'.format(topic)
    
    # getting html result
    r = requests.get(url)
    
    # converting to a bs4 object
    soup = BeautifulSoup(r.content, 'html.parser')
    
    # Empty list that stores list of dictionaries (for each article)
    result = []

    # for each news article block
    for article in soup.find_all('article'):

        try:
            headline = article.find('h3').find('a').text
            source = article.find('a', attrs={'data-n-tid':'9'}).text
            time = article.find('time').attrs['datetime']

            result.append({'searchtopic':topic, 'headline':headline, 'source':source, 'time':time})

        except:
            continue
     
    # return dataframe of results
    return pd.DataFrame(result)

df = pd.DataFrame(columns = ['searchtopic', 'headline', 'source', 'time'])

print('Extracting data from Google News: ')

# For each cryptocurrency 
for topic in topics:
    
    print('Search Topic:', topic, end = ' ')
    
    try:
    
        # Extract the recent 100 news article headlines and store in df
        df_result = extract(topic)

        print('DONE!')
    
    except:
        
        print('FAILED!')
        
    df = pd.concat([df, df_result])

# Load the env variables (EC2 credentials)
load_dotenv()

# Create the connection to Postgres Database in EC2 
POSTGRES_ADDRESS = os.getenv('POSTGRES_ADDRESS')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_USERNAME = os.getenv('POSTGRES_USERNAME')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DBNAME = os.getenv('POSTGRES_DBNAME')

postgres_str = ('postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'.format(username=POSTGRES_USERNAME, \
                                                                                        password=POSTGRES_PASSWORD,\
                                                                                        ipaddress=POSTGRES_ADDRESS,\
                                                                                        port=POSTGRES_PORT,\
                                                                                        dbname=POSTGRES_DBNAME))
cnx = create_engine(postgres_str)

try:
    # Store df in the database as crypto table (Note here replace is used instead of append, which is used ideally)
    df.to_sql('crypto', cnx, index=False, if_exists='append')
    print('Data successfully stored in postgres!')

except:
    print('Error loading data into postgres!')


# Schema for crypto

# CREATE TABLE crypto (
#    newsid INT GENERATED ALWAYS AS IDENTITY,
#    searchtopic VARCHAR(100) NOT NULL,
#    headline VARCHAR(500) NULL,
#    source VARCHAR(100) NULL,
#    time TIMESTAMP NULL
# );


## *Note: For the purpose of simplicity, we currently don't have a unique id for each headline, which is why an auto increment
## identity key is created, but another option we could use is create a unique identifier so that even if articles are repeatedly inserted,
## only a single copy exists for each of them. 