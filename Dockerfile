FROM python:3.11-slim

# System deps
RUN apt-get update && apt-get install -y \
    wget unzip xvfb chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy our app
COPY app/ /app/

# Start headless Chrome in background
CMD ["bash","-lc","xvfb-run -a python whatsapp_bot.py"]
