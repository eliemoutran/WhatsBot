import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep
import re


class Cleverbot:

    def __init__(self):
        self.opts = Options()
        #self.opts.add_argument("--headless")
        self.browser = webdriver.Chrome(options=self.opts)
        self.url = 'https://www.cleverbot.com'
        self.hacking = False
        self.count = -1

    
    def get_form(self):
        while True:
            try:
                self.elem = self.browser.find_element_by_class_name('stimulus')
            except BrokenPipeError:
                continue
            break


    def send_input(self, userInput):
        fOne = '<\/?[a-z]+>|<DOCTYPE'
        fTwo = '/<[^>]+>/g'
        if re.search(fOne, userInput) != None or re.search(fTwo, userInput) != None:
            self.hacking = True
            userInput = 'I will hack you'
        while True:
            try:
                self.elem.send_keys(userInput + Keys.RETURN)
            except BrokenPipeError:
                continue
            break


    def get_response(self):
        while self.hacking == False:
            try:
                while True:
                    try:
                        line = self.browser.find_element_by_id('line1')
                        sleep(3)
                        newLine = self.browser.find_element_by_id('line1')
                        if line.text != newLine and newLine.text != ' ' and newLine.text != '':
                            line = self.browser.find_element_by_id('line1')
                            sleep(3)
                            break
                    except StaleElementReferenceException:
                        self.url = self.url + '/?' + str(int(self.count + 1))
                        continue
            except BrokenPipeError:
                continue
            break
        if self.hacking == True:
            self.botResponse = 'Silly rabbit, html is for skids.'
        elif self.hacking == False:
            self.botResponse = line.text
        self.hacking = False
        return self.botResponse


    def single_exchange(self, userInput):
        while True:
            try:
                self.browser.get(self.url)
            except BrokenPipeError:
                continue
            break
        self.get_form()
        self.send_input(userInput)
        self.get_response()
        return self.botResponse




