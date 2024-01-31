# News Categorization and Classification Documentation

## Overview
This project is designed to collect news articles from an RSS feed, store them in a MySQL database, and categorize them into predefined categories. The categorization is done using the Google Gemini model for natural language understanding.

## Components
The project consists of the following components:

1. **RSS Feed Parser:** Utilizes the `feedparser` library to fetch news articles from the specified RSS feed.

2. **Database Storage:** Uses SQLAlchemy to define a database schema and store news articles in a MySQL database.

3. **Google Gemini Integration:** Integrates with the Google Gemini model through the `genai` library for content generation and categorization.

## Configuration
Before running the code, ensure that you have the necessary dependencies installed. You need to set up a MySQL database and configure the Google Gemini API key.

### Dependencies
- `feedparser`
- `sqlalchemy`
- `google.generativeai`

### Database Connection
Update the `username`, `password`, `host`, `port`, and `database` variables in the code to match your MySQL database connection details.

### Google Gemini API Key
Replace the `api_key` variable with your actual Google Gemini API key.

