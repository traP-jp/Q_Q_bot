from traq_bot import TraqBot
from traq.api import message_api
import traq
import os

from channel import join_channel
from massage import send_message

CONFIGURATION = traq.Configuration(
    host = "https://q.trap.jp/api/v3"
)

CONFIGURATION.access_token = os.environ.get("ACCESS_TOKEN")




bot = TraqBot(os.environ.get("VERIFY_TOKEN"))



@bot.message_created
def message_created(message):
    Q_Q_USER_ID = "c75f0d59-9722-416b-be31-b21375378690"
    for embedded in message["embedded"]:
        # 自分へのメンションを含むか判定
        if embedded.has_key("type") and embedded["type"] == "user" and  embedded["id"] == Q_Q_USER_ID:
            join_channel(message["channelId"], CONFIGURATION)
            send_message(message["channelId"], "Q_Q < :oisu:", CONFIGURATION)
    

if __name__ == '__main__':
    print('Start bot...')
    bot.run(8080)