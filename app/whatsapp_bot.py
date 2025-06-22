import os, pickle, time, datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/contacts.readonly'
]

def get_services():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh()
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as f:
            f.write(creds.to_json())
    return (
        build('calendar', 'v3', credentials=creds),
        build('people', 'v1', credentials=creds)
    )

def get_today_events(cal):
    start = datetime.datetime.combine(datetime.date.today(), datetime.time.min).isoformat() + 'Z'
    end = datetime.datetime.combine(datetime.date.today(), datetime.time.max).isoformat() + 'Z'
    return cal.events().list(
        calendarId='primary', timeMin=start, timeMax=end,
        singleEvents=True, orderBy='startTime'
    ).execute().get('items', [])

def get_contacts(people):
    contacts = {}
    results = people.people().connections().list(
        resourceName='people/me', pageSize=2000,
        personFields='names,phoneNumbers'
    ).execute()
    for p in results.get('connections', []):
        names = p.get('names', [])
        phones = p.get('phoneNumbers', [])
        if names and phones:
            contacts[names[0]['displayName'].lower()] = phones[0]['value'].replace(" ", "")
    return contacts

def init_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    cookie_file = 'cookies.pkl'
    driver.get("https://web.whatsapp.com")
    if os.path.exists(cookie_file):
        for c in pickle.load(open(cookie_file, "rb")):
            driver.add_cookie(c)
        driver.refresh()
    else:
        print("🚨 Scan QR code to login, then press Enter …")
        input()
        pickle.dump(driver.get_cookies(), open(cookie_file, "wb"))
    return driver

def send_message(driver, phone, message):
    url = f"https://web.whatsapp.com/send?phone={phone}&text={message}"
    driver.get(url)
    time.sleep(10)
    try:
        driver.find_element("xpath","//button[@data-testid='compose-btn-send']").click()
        print(f"📤 Sent to {phone}")
    except:
        print("❌ Failed to send to", phone)

def main():
    calendar, people = get_services()
    contacts = get_contacts(people)
    events = get_today_events(calendar)
    driver = init_driver()

    for e in events:
        summary = e.get('summary','').lower()
        for name, phone in contacts.items():
            if name in summary:
                if 'birthday' in summary:
                    msg = f"🎉 Happy Birthday, {name.title()}!"
                elif 'anniversary' in summary:
                    msg = f"💖 Happy Anniversary, {name.title()}!"
                else:
                    msg = f"🎊 Hello, {name.title()}!"
                send_message(driver, phone, msg)
                break

    driver.quit()

if __name__ == '__main__':
    main()
