import requests
from secret import API_KEY, MY_ID, BOT_API
import telebot # pip install pyTelegramBotAPI
from time import sleep
from datetime import datetime
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

PATH = {
    "login": "https://cryptoctf.m0lecon.it",
    "challenges": "https://cryptoctf.m0lecon.it/api/v1/challenges"
}

OLD_CHALLENGES = 32
SLEEP = 60 * 2
END_DATE = datetime(2024, 6, 17, 0, 0, 0)


def main():
    bot = telebot.TeleBot(BOT_API)
    found = False

    def bot_message(message):
        bot.send_message(MY_ID, "[cryptoctf.m0lecon.it] " + message)

    while not found:
        try:
            with requests.Session() as sess:
                print(f"Checking at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}..." + " "*30, end="\r")

                sess.get(PATH["login"], headers={"Authorization": f"Token {API_KEY}", "Content-Type": "application/json"})
                response = sess.get(PATH["challenges"])

                try:
                    response = response.json()
                    if not response["success"]:
                        raise Exception("Failed to get challenges")

                    len_challenges = len(response["data"])

                    if len_challenges > OLD_CHALLENGES: 
                        found = True
                        bot_message(f"{len_challenges-OLD_CHALLENGES} new challenges available")

                except Exception as e:
                    print(f"{e= }")
        
        except Exception as e:
            print(f"{e= }")
            bot_message(f"Error: {e}")
        

        if datetime.now() > END_DATE:
            break

        sleep(SLEEP)

    if found:
        bot_message("Program correctly ended")
    else:
        bot_message("Program ended without finding new challenges")

if __name__ == "__main__":
    main()