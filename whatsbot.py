from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
import cb
import sys
import re

opts = Options()
opts.add_argument("Chrome/28.0.1500.52")
browser = webdriver.Chrome(chrome_options=opts);
browser.get("https://web.whatsapp.com")
friend_name = input("Enter your friend's name: ")
input("Press enter once logged in: ")


def send_message(name, message):
    try:
        send_msg = WebDriverWait(browser, 10).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]")))
        messages = message.split("\n")
        for msg in messages:
            send_msg.send_keys(msg)
            send_msg.send_keys(Keys.SHIFT+Keys.ENTER)
        send_msg.send_keys(Keys.ENTER)
        return True
    except TimeoutException:
        raise TimeoutError("Your request has been timed out! Try overriding timeout!")
    except NoSuchElementException:
        return False
    except Exception:
        return False

def get_last_message_for(name):
    messages = list()
    search = browser.find_element_by_css_selector("#side > div._2EoyP > div > button > div._1MdKA.w-vsN > span")
    search.click()
    sleep(1)
    search= browser.find_element_by_css_selector('#side > div._2EoyP > div > label > div > div._3FRCZ.copyable-text.selectable-text')
    search.send_keys(name+Keys.ENTER)
    
    soup = BeautifulSoup(browser.page_source, "html.parser")
    for i in soup.find_all("div", class_="message-in"):
        message = i.find("span", class_="selectable-text")
        if message:
            message2 = message.find("span")
            if message2:
              messages.append(message2.text)
    messages = list(filter(None, messages))
    return messages

def main():
    cb = cb.Cleverbot()
    try:
        cb.browser.get(cb.url)
    except:
        cb.browser.close()
        sys.exit()
    prev_msg = ''
    while True:
        try:
            cb.get_form()
        except:
            sys.exit()
        userInput=get_last_message_for(friend_name)[-1]
        while(userInput==prev_msg):
            sleep(1)
            userInput=get_last_message_for(friend_name)[-1]
        prev_msg = userInput
        if userInput.lower() == 'quit': # If your friend sends quit the bot will stop
            break
        cb.send_input(userInput)
        bot = cb.get_response()
        sleep(1)
        send_message(friend_name,str(bot))
    cb.browser.close()

if __name__ == "__main__":
    main()
