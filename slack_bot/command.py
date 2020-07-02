from slackclient import SlackClient

# util
TOKEN = "xoxb-1224553073220-1203698095863-Au6LzjuGW79YvY1NhibkNDNn"
slack_client = SlackClient(TOKEN)


# if slack_client.rtm_connect():
#     while True:
#         receive_data = slack_client.rtm_read()
#         if (len(receive_data)):
#             keys = list(receive_data[0].keys())
#