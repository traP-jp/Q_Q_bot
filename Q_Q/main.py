import os

from traq_bot import TraqBot
from traq.api import message_api
import traq
from traq.model.post_message_request import PostMessageRequest

CONFIGURATION = traq.Configuration(
    host = "https://q.trap.jp/api/v3"
)

CONFIGURATION.access_token = os.environ.get("ACCESS_TOKEN")

bot = TraqBot(os.environ.get("VERIFY_TOKEN"))

def subchannels(all_channels, configuration):
    pass


def join_channel(channel_id, configuration):
    pass


def leave_channel(channel_id, configuration):
    pass

def send_message(channel_id, message, configuration):
    message_api.create_message(channel_id, message)
    with traq.ApiClient(configuration) as api_client:
        api_instance = message_api.MessageApi(api_client)
        post_message_request = PostMessageRequest(
            content=message,
            embed=False,
        ) 
    try:
        api_response = api_instance.post_message(channel_id, post_message_request=post_message_request)
    except traq.ApiException as e:
        print("Exception when calling MessageApi->post_message: %s\n" % e)

    return api_response

@bot.message_created
def message_created(message):
    print(message)
    Q_Q_USER_ID = "c75f0d59-9722-416b-be31-b21375378690"
    if "embedded" in message:

        for embedded in message["embedded"]:
            # 自分へのメンションを含むか判定
            if "type" in embedded and embedded["type"] == "user" and embedded["id"] == Q_Q_USER_ID:
                join_channel(message["channelId"], CONFIGURATION)
                send_message(message["channelId"], "Q_Q < :oisu:", CONFIGURATION)
    

if __name__ == '__main__':
    os.system('touch output.log')
    print('Start bot...')
    bot.run(8080)
