import json
import requests
import time
import data_reader_new_1_july

TOKEN = "816974044:AAHuL1mFPnl3mAU6_jIw3OYW0X02Qv47aNE"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    """downloads content from URL and return it as a string"""
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    """gets string and parses this to Python dictionary """
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    """retrieves list of "updates" (messages sent to our Bot)"""
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    """get  chat ID and message text of most recent message sent to Bot"""
    num_updates = len(updates["result"])
    last_update = (num_updates - 1)
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return text, chat_id


def get_last_update_id(updates):
    """calculates highest update ID of all the updates we receive from getUpdates."""
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def answer(updates):
    for update in updates["result"]:
        try:
            user_question = update["message"]["text"]
            print(user_question)
            chat = update["message"]["chat"]["id"]
            print(chat)
            pm_lines_loaded = data_reader_new_1_july.load_file()
            gpm_dict, prince_dict = data_reader_new_1_july.data_to_lists(pm_lines_loaded)
            answer_string = data_reader_new_1_july.choose_pm_dict(user_question,
                                                                      gpm_dict,
                                                                      prince_dict)
            print(answer_string)
            send_message(answer_string,chat)
        except Exception as ex:
            print(ex)


def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            answer(updates)
        time.sleep(0.5)


# lets us import our functions into another script without running anything
if __name__ == '__main__':
    main()
