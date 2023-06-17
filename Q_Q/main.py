import os
import json
import requests
import time
import pprint
import re

from traq_bot import TraqBot
from traq.api import message_api
from traq.api import bot_api
from traq.api import stamp_api
from traq.model.post_message_stamp_request import PostMessageStampRequest
from traq.model.post_bot_action_join_request import PostBotActionJoinRequest
from traq.model.post_bot_action_leave_request import PostBotActionLeaveRequest
import traq
from traq.model.post_message_request import PostMessageRequest

CONFIGURATION = traq.Configuration(
    host = "https://q.trap.jp/api/v3"
)

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")

CONFIGURATION.access_token = os.environ.get("ACCESS_TOKEN")

bot = TraqBot(VERIFY_TOKEN)

Q_Q_USER_ID = "c75f0d59-9722-416b-be31-b21375378690"
Q_Q_BOT_ID = "cc208ab8-4bfa-4de7-9e77-2d76a2721c5b"

STAMP_1_ID = "9f0be841-fbfa-4abf-871e-c1c72627e691"
STAMP_2_ID = "350c45b4-a048-4f62-bf2b-e98f4edef40c"
STAMP_3_ID = "ea0e7725-5b86-456b-b34a-060035153be2"
STAMP_4_ID = "1463cc12-9758-478f-b968-e031a912d426"
STAMP_5_ID = "2d04f8d3-b2db-4e53-b11c-111350c7b70d"
STAMP_6_ID = "4134c613-8e9d-45f8-a8e3-d0f0d464d788"

KAN_ID = "68c4cc50-487d-44a1-ade3-0808023037b8"

NUMBERS_STAMPS = [
    STAMP_1_ID,
    STAMP_2_ID,
    STAMP_3_ID,
    STAMP_4_ID,
    STAMP_5_ID,
    STAMP_6_ID,
]

def search_in(_in, configuration, offset=0):
    with traq.ApiClient(configuration) as api_client:
        api_instance = message_api.MessageApi(api_client)
        try:
            api_response = api_instance.search_messages(word='', offset=offset, _in=_in, sort='createdAt')
        except traq.ApiException as e:
            print("Exception when calling MessageApi->search_messages: %s\n" % e)
    return api_response

def join_channel(channel_id, configuration):
    send_message(channel_id, "Q_Q < Join~!", configuration)
    with traq.ApiClient(configuration) as api_client:
        api_instance = bot_api.BotApi(api_client)
        post_bot_action_join_request = PostBotActionJoinRequest(
            channel_id=channel_id,
        )
        bot_id = Q_Q_BOT_ID
        try:
            api_instance.let_bot_join_channel(bot_id, post_bot_action_join_request=post_bot_action_join_request)
            send_message(channel_id, "Q_Q < done~!", configuration)
        except traq.ApiException as e:
            print("Exception when calling BotApi->let_bot_join_channel: %s\n" % e)
            send_message(channel_id, "Q_Q < failed~! :wara.ex-large:", configuration)
    

def leave_channel(channel_id, configuration):
    send_message(channel_id, "Q_Q < leave~~", configuration)
    print('leadve from', channel_id)
    with traq.ApiClient(configuration) as api_client:
        api_instance = bot_api.BotApi(api_client)
        post_bot_action_leave_request = PostBotActionLeaveRequest(
            channel_id=channel_id,
        )
        bot_id = Q_Q_BOT_ID
        try:
            api_instance.let_bot_leave_channel(bot_id, post_bot_action_leave_request=post_bot_action_leave_request)
            send_message(channel_id, "Q_Q < done~~", configuration)
        except traq.ApiException as e:
            print("Exception when calling BotApi->let_bot_join_channel: %s\n" % e)
            send_message(channel_id, "Q_Q < failed~~ :wara.ex-large:", configuration)


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


def load_channles():
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
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
    
def collect_children(channel_id, configuration):
    all_channel = load_channles()
    children = {}
    for channel in all_channel['public']:
        if (channel["parentId"] == channel_id) and (isnumber(channel["name"])):
            children[channel["name"]] = channel["id"]
    return children


def add_message_stamp(message_id, stamp_id, configuration):
    print('add stamp')
    with traq.ApiClient(configuration) as api_client:
        api_instance = stamp_api.StampApi(api_client)
        print('instance')
        post_message_stamp_request = PostMessageStampRequest(
            count=1,
        )
        print('pos')
        try:
            print('try')
            api_instance.add_message_stamp(message_id, stamp_id, post_message_stamp_request=post_message_stamp_request)
        except traq.ApiException as e:
            print("Exception when calling StampApi->add_message_stamp: %s\n" % e)


@bot.message_created
def message_created(message):
    pprint.pprint(message)
    message = message['message']
    
    # === joinを判定する部分 ===
    if "embedded" in message:
        for embedded in message["embedded"]:
            # 自分へのメンションを含むか判定
            if "type" in embedded and embedded["type"] == "user" and embedded["id"] == Q_Q_USER_ID:
                # joinを含むか判定
                if "join" in message["plainText"]:
                    join_channel(message["channelId"], CONFIGURATION)
                    children = collect_children(message["channelId"], CONFIGURATION)
                    send_message(message["channelId"], "Q_Q < :oisu:", CONFIGURATION)
                    return
                elif "leave" in message["plainText"]:
                    leave_channel(message["channelId"], CONFIGURATION)
                    return

    # === 質問割り振り部分 ===
    channel_id = message['channelId']
    children_channels = collect_children(channel_id, CONFIGURATION)
    final_message_time = {}
    for ch_name, ch_id in children_channels.items():
        ch_message = search_in(ch_id, CONFIGURATION)
        newest_message = ch_message['hits'][0]
        final_message_time[ch_name] = newest_message['created_at']

    final_message_time = sorted(final_message_time.items(), key = lambda v : v[1])
    select_channel_number = final_message_time[0][0]
    selected_chhannel_id = children_channels[select_channel_number]
    stamp = NUMBERS_STAMPS[int(select_channel_number) - 1]
    message_id = message['id']
    add_message_stamp(message_id, stamp, CONFIGURATION)
    send_message(
                selected_chhannel_id,
                "https://q.trap.jp/messages/" + message_id,
                CONFIGURATION
    )        

    time.sleep(1)
    return
    

def get_message(message_id, configuration):
    with traq.ApiClient(configuration) as api_client:
        api_instance = message_api.MessageApi(api_client)
        try:
            api_response = api_instance.get_message(message_id)
        except traq.ApiException as e:
            print("Exception when calling MessageApi->get_message: %s\n" % e)

    return api_response


@bot.bot_message_stamps_updated
def stamps_updated(data):
    pprint.pprint(data)
    message_id = data['messageId']
    for stamp in data['stamps']:
        if stamp['stampId'] == KAN_ID:
            message = get_message(message_id, CONFIGURATION)
            pprint.pprint(message)
            quote = r"https://q\.trap\.jp/messages/([a-zA-Z0-9-]+)"

            match = re.search(quote, message['content'])
            if match:
                add_message_stamp(match.group(1), KAN_ID, CONFIGURATION)


if __name__ == '__main__':
    print('Start bot...')
    bot.run(80)
