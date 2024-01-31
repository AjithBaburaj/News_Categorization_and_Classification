import feedparser
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote
import datetime
import time
import google.generativeai as genai

import google.generativeai as genai
## Configure Genai Key
api_key = "AIzaSyA56QV0jwvxrFTh6-Cs-Lt1qJ1QxukfC9Q"
genai.configure(api_key=api_key)

rss_feed_url = 'http://rss.cnn.com/rss/cnn_topstories.rss'

# Define the SQLAlchemy model
Base = declarative_base()

class NewsArticle(Base):
    __tablename__ = 'news_articles'
    id = Column(Integer, primary_key=True)
    title = Column(String(length=255))
    published = Column(DateTime)  # Updated to DateTime type
    summary = Column(String(length=500))
    url = Column(String(length=500))
    category = Column(Integer)
    category_name = Column(String(length=50))

# Replace with your actual connection details
username = 'root'
password = 'Ajith@123'
host = 'localhost'
port = '3306'
database = 'rss_data'

# Quote the password to handle special characters
quoted_password = quote(password, safe='')

# Construct the connection string
connection_string = f'mysql://{username}:{quoted_password}@{host}:{port}/{database}'


# Parse the RSS feed
feed = feedparser.parse(rss_feed_url)

# Set up the database connection
engine = create_engine(connection_string)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Iterate through the entries and store them in the database
for entry in feed.entries:
    title = entry.get('title', 'N/A')
    # Convert time.struct_time to datetime
    published = datetime.datetime.fromtimestamp(time.mktime(entry.get('published_parsed', datetime.datetime.now().timetuple())))
    summary = entry.get('summary', 'N/A')
    url = entry.get('link', 'N/A')

    # Create a NewsArticle object and add it to the session
    article = NewsArticle(title=title, published=published, summary=summary, url=url)
    session.add(article)

# Commit the changes to the database
session.commit()



## Function To Load Google Gemini Model and provide queries as response

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

## Define Your Prompt
prompt=[
    """classify the given text to anyof the following categories based on the context.
    Categories:
    1.Terrorism / protest / political unrest / riot
    2.Positive/Uplifting
    3.Natural Disasters
    4.others
    output format : give only the category number as output
    """


]



# Define the mapping between numeric categories and category names
category_mapping = {
    1: "Terrorism / Protest / Political Unrest / Riot",
    2: "Positive/Uplifting",
    3: "Natural Disasters",
    4: "Others"
}

# Iterate through the stored articles and apply classification and Gemini response
for entry in session.query(NewsArticle):
    title = entry.title
    summary = entry.summary
    input_text = f"{title} {summary}"
    
    # Get the numeric category from get_gemini_response
    numeric_category = int(get_gemini_response(input_text, prompt))
    
    # Map the numeric category to its corresponding category name
    category_name = category_mapping.get(numeric_category, "Unknown")
    
    # Update the category columns in the database
    entry.category = numeric_category
    entry.category_name = category_name

# Commit the changes to the database
session.commit()


# Close the session
session.close()
