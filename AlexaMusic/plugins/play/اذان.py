import requests
import datetime
import threading
import time
from AlexaMusic import app
from pyrogram import Client, filters
from pyrogram.types import Message
url = "http://api.aladhan.com/timingsByAddress?address=Cairo&method=4&school=0"


# بدلها بالمستخدمين عندك
users = [1748768168]

prayers = {
    "Fajr" : "الفجر", 
    "Dhuhr" : "الضهر", 
    "Asr" : "العصر", 
    "Maghrib" : "المغرب", 
    "Isha" : "العشاء"
    }

@client.on_message(filters.command("تفعيل الصلاه", ""))
def enable_prayer(bot: Client, message: Message):
    chat_id = message.chat.id
    if chat_id not in users:
        users.append(chat_id)
        message.reply_text("تم تفعيل الصلاه 👀")
        return
    message.reply_text("متفعله يسطا")

@client.on_message(filters.command("تعطيل الصلاه", ""))
def disable_prayer(bot: Client, message: Message):
    chat_id = message.chat.id
    if chat_id in users:
        users.remove(chat_id)
        message.reply_text("تم تعطيل الصلاه 👀")
        return
    message.reply_text("ماهي مش متفعله يسطا")
    
def main():
    for prayer in prayers:
        thread = threading.Thread(target=loop, args=(prayer, prayers[prayer], ))
        thread.start()

def loop(prayer, name):
    while True:
        if len(users) == 0:
            continue
        response = requests.get(url).json()
        timer = response["data"]["timings"][prayer].split(":")
        broadcast_time = str(datetime.time(hour=int(timer[0]), minute=int(timer[1])).strftime("%H:%M"))
        current_time = str(datetime.datetime.now().strftime("%H:%M"))
        if current_time == broadcast_time:
            for user in users:
                client.send_message(
                    user,
                    f"حان الآن موعد آذان {name} بتوقيت القاهره ❤"
                )
            time.sleep(60)
        time.sleep(2)

if __name__ == "__main__":
    main()
    client.run()
