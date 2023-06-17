import os
import json

from traq_bot import TraqBot
from traq.api import message_api
from traq.api import bot_api
from traq.model.post_bot_action_join_request import PostBotActionJoinRequest
import requests


import traq
from traq.model.post_message_request import PostMessageRequest

CONFIGURATION = traq.Configuration(
    host = "https://q.trap.jp/api/v3"
)

CONFIGURATION.access_token = os.environ.get("ACCESS_TOKEN")

bot = TraqBot(os.environ.get("VERIFY_TOKEN"))


Q_Q_USER_ID = "c75f0d59-9722-416b-be31-b21375378690"

def subchannels(all_channels, configuration):
    pass


def join_channel(channel_id, configuration):
    with traq.ApiClient(configuration) as api_client:
        api_instance = bot_api.BotApi(api_client)
        bot_id = Q_Q_USER_ID
        post_bot_action_join_request = PostBotActionJoinRequest(
            channel_id=channel_id,
        ) 
        try:
            api_instance.let_bot_join_channel(bot_id)
        except traq.ApiException as e:
            print("Exception when calling BotApi->let_bot_join_channel: %s\n" % e)
        try:
            api_instance.let_bot_join_channel(bot_id)
        except traq.ApiException as e:
            print("Exception when calling BotApi->let_bot_join_channel: %s\n" % e)

    send_message(channel_id, "Q_Q < Join~!", configuration)


def leave_channel(channel_id, configuration):
    pass

def send_message(channel_id, message, configuration):
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



# チャンネルリストを取得する
def load_channles():
    access_token = os.environ.get("ACCESS_TOKEN")
    headers = {
        "Authorization": f"Bearer crWzVZn1oYneExkQuAoVoCG1INpZCGuCuyrw",
        "Content-Type": "application/json",
    }

    res = requests.get(
        "https://q.trap.jp/api/v3/channels",
        headers=headers,
    )

    return res.json()


def isnumber(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
def collect_channel(channel_id, configuration):
    all_channel = load_channles()
    children = {}
    for channel in all_channel:
        if channel["parentId"] == channel_id and isnumber(channel["name"]):
            print("join for id:", channel["id"], "name:", channel["name"])
            join_channel(channel["id"], configuration)
            children[channel["name"]] = channel["id"]

    return children



@bot.message_created
def message_created(message):
    print(message)
    message = message['message']
    if "embedded" in message:
        print()
        for embedded in message["embedded"]:
            # 自分へのメンションを含むか判定
            if "type" in embedded and embedded["type"] == "user" and embedded["id"] == Q_Q_USER_ID:
                join_channel(message["channelId"], CONFIGURATION)
                children = collect_channel(message["channelId"], CONFIGURATION)
                send_message(message["channelId"], "Q_Q < :oisu:", CONFIGURATION)
                log_channel(
                    message["channelId"], children
                )

# dump as json
def log_channel(add_parent_id, add_children, to_file):
    # read to_file
    with open(to_file, "r") as f:
        data = json.load(f)

    data[add_parent_id] = add_children

    # write to_file
    with open(to_file, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    os.system('touch output.log')
    print('Start bot...')
    bot.run(8080)
