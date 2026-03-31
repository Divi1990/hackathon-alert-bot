import requests
from datetime import datetime

# 🔑 Replace with your values
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=payload)


def send_alerts():
    url = "https://unstop.com/api/public/opportunity/search-result"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    params = {
        "opportunity": "hackathons",
        "per_page": 10
    }

    response = requests.get(url, headers=headers, params=params)

    print(response.text)  # DEBUG

    if response.status_code != 200:
        print("Error:", response.status_code)
        return

    data = response.json()["data"]["data"]

    today = datetime.today()

    for h in data:
        if h.get("end_date"):

            deadline = datetime.fromisoformat(h["end_date"].split("T")[0])
            diff = (deadline - today).days

            if 0 <= diff <= 5:

                title = h.get("title", "No Title")
                org = h.get("organisation", {}).get("name", "Unknown")
                link = "https://unstop.com" + h.get("public_url", "")

                message = (
                    "🚨 Hackathon Alert!\n\n"
                    f"🎯 {title}\n"
                    f"📅 Deadline: {deadline.strftime('%Y-%m-%d')}\n"
                    f"🏢 {org}\n"
                    f"🔗 {link}"
                )

                print(message)  # DEBUG
                send_telegram(message)


# 🚀 RUN
send_alerts()
