import traq
from traq.api import message_api
from traq.model.post_message_request import PostMessageRequest

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