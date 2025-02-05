import requests
import time

# Base URL
BASE_URL = "https://api-prod.grip.events/1/container/7888/search/extension/93167"

# Headers
HEADERS = {
    "accept": "application/json",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-gb",
    "cache-control": "No-Cache",
    "content-type": "application/json",
    "login-source": "web",
    "origin": "https://discover.medtrade.com",
    "pragma": "No-Cache",
    "priority": "u=1, i",
    "referer": "https://discover.medtrade.com/medtrade2025/app/home/network/list/93167?page=1&sort=name",
    "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "version": "37.0.0",
    "x-authorization": "98fff295-8151-4133-b834-68d18d5583dd",
    "x-grip-version": "Web/37.0.0"
}

# Output file
OUTPUT_FILE = "search_ids.txt"


def scrape_ids():
    with open(OUTPUT_FILE, "w") as file:
        for page in range(1, 87):  
            url = f"{BASE_URL}?order=asc&page={page}&sort=name"
            response = requests.get(url, headers=HEADERS)

            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get("success"):
                        ids = [str(item["id"]) for item in data.get("data", [])]
                        file.write("\n".join(ids) + "\n")  
                        print(f"Page {page}: {len(ids)} IDs saved.")
                    else:
                        print(f"Page {page}: Request successful but 'success' field is False.")
                except Exception as e:
                    print(f"Page {page}: JSON parse error - {e}")
            else:
                print(f"Page {page}: Request failed ")
            time.sleep(3)  

if __name__ == "__main__":
    scrape_ids()