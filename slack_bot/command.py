from slackclient import SlackClient

# util
TOKEN = "xoxb-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
slack_client = SlackClient(TOKEN)


# if slack_client.rtm_connect():
#     while True:
#         receive_data = slack_client.rtm_read()
#         if (len(receive_data)):
#             keys = list(receive_data[0].keys())
#
