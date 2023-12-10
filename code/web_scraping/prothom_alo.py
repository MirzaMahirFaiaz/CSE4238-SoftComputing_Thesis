import requests
import pandas as pd
import datetime
import pytz

def convert_timestamp_to_local(timestamp_ms, timezone="Asia/Dhaka"):
    timestamp_seconds = timestamp_ms / 1000
    utc_dt = datetime.datetime.utcfromtimestamp(timestamp_seconds)
    local_timezone = pytz.timezone(timezone)
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    return local_dt

def scrape_prothomalo_api(url):
    offset = 0
    limit = 10
    all_data = []

    while True:
        # Make GET request to the API
        response = requests.get(f"{url}?offset={offset}&limit={limit}")

        # Check if the response is successful
        if response.status_code == 200:
            data = response.json()
            if not data['items'] or len(data['items']) == 0:
                break  # No more data, exit the loop

            # Append data to the list
            for item in data['items']:
              news_data = {
                  "headline": item['story']['headline'],
                  "summary": item['story']['summary'],
                  "published_at": str(convert_timestamp_to_local(item['story']['published-at']).strftime('%d-%m-%Y')),
                  "url": item['story']['url']
              }
              all_data.append(news_data)

            print(f"{offset + limit} data collected")
            offset += limit
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            break
    return all_data

def export_to_excel(data):
    # Convert data to a Pandas DataFrame
    df = pd.DataFrame(data)

    # Export DataFrame to an Excel file
    df.to_excel('prothomalo_data.xlsx', index=False)
    print("Data exported to prothomalo_data.xlsx")

def export_to_csv(data):
    # Convert data to a Pandas DataFrame
    df = pd.DataFrame(data)

    # Export DataFrame to an Excel file
    df.to_csv('prothomalo_data.csv', index=False)
    print("Data exported to prothomalo_data.csv")

if __name__ == "__main__":
    api_url = "https://www.prothomalo.com/api/v1/collections/stockexchange"
    scraped_data = scrape_prothomalo_api(api_url)
    if scraped_data:
        export_to_csv(scraped_data)
