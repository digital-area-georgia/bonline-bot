from slacker import Slacker
#load environment
import dotenv, os
dotenv.load_dotenv()

# Slack Auth
slack = Slacker(os.getenv('slackerToken'))

if slack.api.test().successful:
    print(
        f"Slacker Connected to {slack.team.info().body['team']['name']}.")
else:
    print('slacker failed to connect, try again!')


def send_slack_alert(message):
    slack.chat.post_message(channel=os.getenv('slackerChannel'),
                            text=message,
                            username=os.getenv('slackerUsername'),
                            icon_emoji=':shopping_trolley:')