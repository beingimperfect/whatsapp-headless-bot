## WhatsApp Headless Bot

### 🚀 Setup
1. Enable Google Calendar & People API, download `credentials.json`
2. Place `credentials.json` into `app/`
3. Build Docker: `docker build -t whatsapp-bot .`
4. First run: `docker run -it -v "$PWD/app:/app" whatsapp-bot`
Scan the WhatsApp Web QR when prompted. Press Enter when done.

### ⏰ Automate
- Cron (local/cloud VM): `0 9 * * * docker run --rm -v "/your/dir/app:/app" whatsapp-bot`

- Cloud Run / ECS: Deploy container; schedule triggers via Cloud Scheduler / EventBridge.


