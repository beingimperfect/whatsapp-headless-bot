# 📬 WhatsApp Headless Bot – Birthday & Anniversary Wishes Automation 🎉

Automatically send personalized WhatsApp messages to your friends and family for birthdays and anniversaries — using Google Calendar, Google Contacts, and WhatsApp Web — all from a headless, cloud-ready Python bot powered by Docker & Selenium.

---

## 🔧 Features

- 🗓️ **Google Calendar Integration**  
  Reads birthday and anniversary events from your calendar.

- 📇 **Google Contacts Integration**  
  Matches events to contacts and fetches their phone numbers.

- 🤖 **Sends WhatsApp Messages Automatically**  
  Uses WhatsApp Web with headless Selenium and persistent login via QR code.

- 🐳 **Dockerized & Headless**  
  Runs seamlessly on local machines, servers, or cloud platforms without GUI.

- ☁️ **Cloud-Ready**  
  Deploy on GCP Cloud Run, AWS ECS, or any Docker-compatible host.

- ⏰ **Cron-Friendly**  
  Schedule daily runs with system cron or Cloud Scheduler.

---

## 📦 Tech Stack

- Python 3.11  
- Selenium + Headless Chrome  
- Google Calendar & People API  
- Docker (xvfb for headless browser)  
- WhatsApp Web (QR login stored via cookies)  

---

## 🚀 Setup

1. **Enable APIs & Download Credentials**

   - Go to the [Google Cloud Console API Library](https://console.cloud.google.com/apis/library).
   - Enable both **Google Calendar API** and **Google People API**.
   - Create OAuth 2.0 credentials for a **Desktop app**.
   - Download the `credentials.json` file.

2. **Add Credentials**

   - Place the downloaded `credentials.json` inside the `app/` directory of your project.

3. **Build Docker Image**

   ```docker build -t whatsapp-bot .```

4. **Run Container for First-Time Login**

    - Run the container interactively and mount the local app/ directory: ```docker run -it -v "$PWD/app:/app" whatsapp-bot```
    - When WhatsApp Web opens, scan the QR code with your phone.
    - After successful login, press Enter in the terminal to save cookies.

5. **Automated Runs**

    - After the first login, you can run the container normally or schedule it via cron or cloud schedulers.
        Example cron job to run daily at 9 AM: ```0 9 * * * docker run --rm -v "/full/path/to/app:/app" whatsapp-bot```

    - Cloud Run / ECS: Deploy container; schedule triggers via Cloud Scheduler / EventBridge.

---

## 📄 How It Works

1. 🎯 Checks your Google Calendar for events today.  
2. 🔍 Matches the event name with your Google Contacts.  
3. 📱 Opens WhatsApp Web in a headless browser.  
4. 💬 Sends a pre-written message to the matched contact automatically.

---

## 🚀 Use Cases

- Automate birthday/anniversary greetings  
- Set and forget: Runs silently every morning  
- Personal but automated outreach for teams, families, small businesses  

---

## 🔐 Disclaimer

This bot uses **your own WhatsApp Web session** — no third-party API keys or automation breaking WhatsApp's terms of service. Use responsibly.




