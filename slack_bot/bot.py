import re
import time


import random
import pandas as pd
import numpy as np

from slack_bot.command import slack_client
from slack_bot.similarity import cos_similarity

RTM_READ_DELAY = 0.6 # delay between reading from RTM
EXAMPLE_COMMAND = "!"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

starterbot_id = None

def parse_bot_commands(slack_events):
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"], event["user"]
    return None, None, None

def parse_direct_mention(message_text):
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel, user):
    default_response = "ex)!호날두, 모라타"
    response = None
    if command.startswith(EXAMPLE_COMMAND):
        try:
            response = cos_similarity(command)
        except:
            response = "다른 선수를 입력해주세요"
        if response == None:
            response = "유효하지 않은 명령어입니다"
    # Send the response back to the channel
    slack_client.api_call("chat.postMessage", channel = channel,
                          text = response or default_response)
if __name__ =="__main__":
    if slack_client.rtm_connect(with_team_state = False):
        print("Bot connected and running!!!")
        startbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel, user = parse_bot_commands(slack_client.rtm_read())
            if command:
                start = time.time()
                handle_command(command, channel, user)
                taken_time = round(time.time() - start, 3)
                text_format = "Taken time: {} seconds".format(taken_time)
                slack_client.api_call("chat.postMessage", channel=channel, text=text_format)
            time.sleep(RTM_READ_DELAY)
        else:
            print("Connection failed. Exception traceback printed above.")