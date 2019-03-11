import click
from slackclient import SlackClient

DEFAULT_MESSAGE = "Hello! I am currently out of office."

@click.command()
@click.option("--username", required=True, help="The user who is going out of office.", envvar="SLACKOOO_USER")
@click.option("--token", required=True, help="Your legacy API token", envvar="SLACKOOO_LEGACY_TOKEN")
@click.option("--response", help="the out of office message you would like to send.", default=DEFAULT_MESSAGE, envvar="SLACKOOO_RESPONSE")
def initialize(username, token, response):
    sc = SlackClient(token)
    username, first_name = get_user_id_and_first_name_for_username(sc, username)
    if not sc.rtm_connect():
        raise Exception("Couldnt hit slack!")
    while True:
        for slack_event in sc.rtm_read():
            if not slack_event.get("type") == "message":
                continue

            message = slack_event.get("text")
            if message is not None and username in message:
                sc.rtm_send_message(slack_event.get("channel"), response)

def get_user_id_and_first_name_for_username(sc, username):
    users = sc.api_call("users.list")
    username = username.replace("@", "").lower()
    user_data = [(user["id"],user["real_name"].split()[0]) for user in users["members"] if user["name"] == username]
    if len(user_data) > 0:
        return user_data[0]
    else:
        raise Exception("We couldnt find your user, sorry!")


if __name__ == "__main__":
    initialize()
