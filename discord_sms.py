import sys
import discord
from discord.ext import commands
import datetime
from twilio.rest import Client
import signal
import time
from datetime import datetime, timedelta, timezone

BOT_TOKEN = ''

ACCOUNT_SID = ''
AUTH_TOKEN = ''

FROM_NUMBER = ""
TO_NUMBER = ""


bot = commands.Bot(command_prefix='!', self_bot=True)
today = datetime.now()

# send_sms sends a SMS with the text using Twilio API
def send_sms(text):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    try:
        message = client.messages.create(
            body=text,
            from_=FROM_NUMBER,
            to=TO_NUMBER
        )
        print(f"SMS Sent with SID: {message.sid}")
    except Exception as e:
        print(f"Error sending SMS: {str(e)}")

# on_ready prints in the console when bot connected
@bot.event
async def on_ready():
    print('Logger is online!')
    print('-' * 50)

# on_message logs messages in the console
@bot.event
async def on_message(msg):
    timestamp = msg.created_at.timestamp()
    date = datetime.fromtimestamp(timestamp)
    text = f"{date.strftime('%H:%M:%S')} | {msg.author.name}: {msg.content}"

    print(text)
    if isinstance(msg.channel, discord.DMChannel):
        if msg.author.name != "MY_USERNAME":
            send_sms(text)

# shutdown_handler handles graceful shutdown 
def shutdown_handler(signal, frame):
    print("Shutting down...")
  
    bot.loop.run_until_complete(bot.logout())
    sys.exit(0)

def main():
  # if not a workday, exit
  if (today.weekday() >= 5) or not (8 < today.hour < 17):
      sys.exit(0)

  # register the shutdown handler for SIGINT signal (CTRL-C)
  signal.signal(signal.SIGINT, shutdown_handler)
  
  bot.run(BOT_TOKEN)


if __name__ == "__main__":
  main()
  
