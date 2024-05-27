import requests
import pandas as pd
from datetime import datetime
import time

# Function to make the HTTP request and get the data
def fetch_news_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve data")
        return None

# Function to present the main attributes of the news
def present_news(data, displayed_news_ids, news_df):
    if data is None:
        return news_df

    new_rows = []

    for news in data:
        news_id = news.get('id')
        if news_id in displayed_news_ids:
            continue  # Skip already displayed news

        title = news.get('titulo')
        description = news.get('descricao')
        news_url = news.get('url')
        publication_date = news.get('data')
        author = news['autores'][0].get('nome') if news['autores'] else 'Unknown'
        image_url = news.get('multimediaPrincipal')
        tags = ", ".join(tag.get('nome') for tag in news.get('tags', []))

        # Format the date
        publication_date = datetime.fromisoformat(publication_date).strftime('%d %B %Y')

        # Assemble the formatted output
        output = f"""
        Title: {title}
        
        Description: {description}
        
        Publication Date: {publication_date}
        
        Author: {author}
        
        Main Image: {image_url}
        
        Tags: {tags}
        
        Read more: {news_url}
        """
        
        # Print the output
        print(output)

        # Prepare the new row
        new_row = {
            'ID': news_id,
            'Title': title,
            'Description': description,
            'URL': news_url,
            'Publication Date': publication_date,
            'Author': author,
            'Main Image': image_url,
            'Tags': tags
        }

        # Append the new row to the list of new rows
        new_rows.append(new_row)

        # Add news ID to the set of displayed news
        displayed_news_ids.add(news_id)

    # Concatenate the new rows to the DataFrame
    if new_rows:
        news_df = pd.concat([news_df, pd.DataFrame(new_rows)], ignore_index=True)

    return news_df

# API URL
api_url = "https://www.publico.pt/api/list/ultimas"

# Set to keep track of displayed news IDs
displayed_news_ids = set()

# DataFrame to store news
news_df = pd.DataFrame(columns=['ID', 'Title', 'Description', 'URL', 'Publication Date', 'Author', 'Main Image', 'Tags'])

# Check for new news every minute
while True:
    # Fetch the news data
    news_data = fetch_news_data(api_url)

    # Present the news and update the DataFrame
    news_df = present_news(news_data, displayed_news_ids, news_df)

    # Save the DataFrame to a CSV file periodically
    news_df.to_csv('news_data.csv', index=False)

    # Wait for 60 seconds before checking again
    time.sleep(60)



