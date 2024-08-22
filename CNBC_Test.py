from bs4 import BeautifulSoup
import requests
import csv
import os

# Function to scrape CNBC latest news and store in CSV
def scrape_and_store_news():
    # URL of the CNBC latest news page
    url = "https://www.cnbc.com/world/?region=world"

    # Send a GET request to fetch the raw HTML content
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the list containing the latest news items
    news_list = soup.find("ul", class_="LatestNews-list")

    # Check if the news list is found
    if news_list:
        # Initialize a list to store news data
        news_data = []

        # Iterate through each news item in the list
        for item in news_list.find_all("li", class_="LatestNews-item"):
            # Find the anchor tag for the news headline and URL
            headline_tag = item.find("a", class_="LatestNews-headline")
            # Find the time tag for the news timestamp
            time_tag = item.find("time", class_="LatestNews-timestamp")

            # Check if both headline and time tags are found
            if headline_tag and time_tag:
                # Extract the news headline text
                headline = headline_tag.get_text(strip=True)
                # Extract the URL of the news article
                url = headline_tag.get("href")
                # Extract the timestamp of the news article
                timestamp = time_tag.get_text(strip=True)

                # Append the data as a dictionary
                news_data.append({
                    'Time': timestamp,
                    'Headline': headline,
                    'URL': url
                })

        # Specify the path to the CSV file and create the CNBC folder if it doesn't exist
        folder_name = 'CNBC'
        os.makedirs(folder_name, exist_ok=True)
        csv_file = os.path.join(folder_name, 'cnbc_latest_news.csv')

        # Write the data to CSV file
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['Time', 'Headline', 'URL']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Write headers
            writer.writeheader()

            # Write rows
            for news_item in news_data:
                writer.writerow(news_item)

        print(f"CSV file '{csv_file}' has been successfully created with the latest CNBC news.")
    else:
        print("Failed to find the parent div containing the news list.")

# Call the function to scrape and store CNBC latest news in CSV
scrape_and_store_news()
