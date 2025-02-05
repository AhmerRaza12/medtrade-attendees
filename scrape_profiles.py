import requests
import time
import os
import pandas as pd
import json

BASE_URL="https://api-prod.grip.events/1/container/7888/thing"

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

def appendProduct(file_path2, data):
    temp_file = 'temp_file.csv'
    if os.path.isfile(file_path2):
        df = pd.read_csv(file_path2, encoding='utf-8')
    else:
        df = pd.DataFrame()

    df_new_row = pd.DataFrame([data])
    df = pd.concat([df, df_new_row], ignore_index=True)

    try:
        df.to_csv(temp_file, index=False, encoding='utf-8')
    except Exception as e:
        print(f"An error occurred while saving the temporary file: {str(e)}")
        return False

    try:
        os.replace(temp_file, file_path2)
    except Exception as e:
        print(f"An error occurred while replacing the original file: {str(e)}")
        return False

    return True

def extract_linkedin_url(rtm_string):
    try:
        rtm_data = json.loads(rtm_string)  # Parse the JSON string inside rtm
        for key, value in rtm_data.items():
            if value.get("label") == "Company URLs":  # Check if label is "Company URLs"
                return value.get("sentence", "")  # Return the sentence (which contains the URL)
    except json.JSONDecodeError:
        print("Error decoding rtm JSON")
    return ""





def scrape_ids(ids):
    profiles = []
    for id in ids:
        print(f"Scraping profile {id}")
        url = f"{BASE_URL}/{id}"
        response = requests.get(url, headers=HEADERS)
        # in response.json() we have the data
        if response.status_code == 200:
            try:
                data = response.json()
                if data.get("success"):
                    attendee_data = data.get("data", {})
                    name=attendee_data.get("name", " ")
                    job_title=attendee_data.get("job_title", " ")
                    company_name=attendee_data.get("company_name", " ")
                    location=attendee_data.get("location", " ")
                    summary=attendee_data.get("summary", " ")
                    rtm=attendee_data.get("rtm", "{}")
                    linkedin_url=extract_linkedin_url(rtm)
                    profile = {
                        "Attendee Id": id,
                        "Attendee Name": name,
                        "Attendee Job Title": job_title,
                        "Attendee Company Name": company_name,
                        "Attendee Summary": summary,
                        "Attendee Location": location,
                        "Attendee LinkedIn/Company URL": linkedin_url
                    }
                    print("Profile scraped:", profile)
                    appendProduct('attendee_profiles.csv', profile)
                    profiles.append(profile)
                else:
                    print(f"Profile {id}: Request successful but 'success' field is False.")
            except Exception as e:
                print(f"Profile {id}: JSON parse error - {e}")
        else:
            print(f"Profile {id}: Request failed ")
        time.sleep(2)
    return profiles  

if __name__ == "__main__":
    ids=[]
    with open("search_ids.txt") as file:
        for line in file:
            ids.append(line.strip())
    attended_profiles = scrape_ids(ids)
    print("Profiles scraped:", len(attended_profiles))
    