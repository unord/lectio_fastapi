import time
import requests
import bs4
from decouple import config
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import datetime
import sys
from typing import List
import json



def lectio_login(school_id :int, lectio_user :str, lectio_password :str, browser):
    max_try_attempts = 100

    this_url = f"https://www.lectio.dk/lectio/{school_id}/login.aspx"

    #go to login page
    try:
        browser.get(this_url)
    except:
        return {'msg': 'Could not load page', 'success': False}

    #insert username in lectio login, user field
    try_attempt = 0
    while try_attempt != max_try_attempts:
        try:
            input_username = browser.find_element("id", "username")
            input_username.send_keys(lectio_user)
            try_attempt = max_try_attempts
        except NoSuchElementException:
            if try_attempt == max_try_attempts-1:
                return {'msg': 'Could not insert username on login page. Reason maybe webpage is not being loaded correctly.', 'success': False}
            try_attempt += 1

    #insert password in lectio login page, password field
    try_attempt = 0
    while try_attempt != max_try_attempts:
        try:
            input_password = browser.find_element("id", "password")
            input_password.send_keys(lectio_password)
            try_attempt = max_try_attempts
        except NoSuchElementException:
            if try_attempt == max_try_attempts-1:
                return {'msg': 'Could not insert password on login page. Reason maybe webpage is not being loaded correctly.', 'success': False}
            try_attempt += 1

    try_attempt = 0
    while try_attempt != max_try_attempts:
        try:
            button_login = browser.find_element("id", "m_Content_submitbtn2")
            button_login.click()
            try_attempt = max_try_attempts
        except NoSuchElementException:
            if try_attempt == max_try_attempts-1:
                return {'msg': 'Could not push the login button. Reason maybe webpage is not being loaded correctly.', 'success': False}
            try_attempt = try_attempt + 1

    time.sleep(1)
    browser.get(f"https://www.lectio.dk/lectio/{school_id}/forside.aspx")
    try:
        current_user = browser.find_element("id", "s_m_LoginOutLink").text
        return {'msg': 'Login successful', 'success': True}
    except NoSuchElementException as e:
        print(e)
        return {'msg': 'Login failed, wrong username, password and school_id combination ', 'success': False}

def lectio_send_msg(browser, this_team, this_msg, disbale_send=False):
    now = datetime.datetime.now()
    #this_team = lectio_test_class #For test only
    this_subject = f"Fagevalueringsundersøgelse for hold: {this_team}"

    # go to lectio send message page
    try:
        browser.get(lectio_url_send_msg)
    except:
        error_msg = "FAG_eval_rpa crashed when trying to access lectio send message page"
        log.log("FAG_eval_rpa crashed when trying to access lectio send message page")
        send_sms.sms_troubleshooters(error_msg)
        sys.exit()

    # insert class in "to field"
    try_attempt = 0
    while try_attempt != max_try_attempts:
        try:
            input_class_name = browser.find_element_by_id("s_m_Content_Content_addRecipientDD_inp")
            input_class_name.send_keys(this_team)
            input_class_name.send_keys(Keys.ARROW_DOWN)
            input_class_name.send_keys(Keys.ARROW_DOWN)
            if this_team == "hvhh1c Vø":
                input_class_name.send_keys(Keys.ARROW_DOWN)

            input_class_name.send_keys(Keys.ENTER)
            try_attempt = max_try_attempts
        except NoSuchElementException:
            if try_attempt == max_try_attempts - 1:
                error_msg = f"{now}: FAG_eval_rpa crashed when trying to type the class_name in lectio send message page"
                log.log("FAG_eval_rpa crashed when trying to type the class_name in lectio send message page")
                send_sms.sms_troubleshooters(error_msg)
                sys.exit()
            try_attempt = try_attempt + 1

    # insert message in "subject field"
    try_attempt = 0
    while try_attempt != max_try_attempts:
        try:
            input_subject = browser.find_element_by_id("s_m_Content_Content_CreateThreadEditMessageTitle_tb")
            input_subject.send_keys(this_subject)
            try_attempt = max_try_attempts
        except NoSuchElementException:
            if try_attempt == max_try_attempts - 1:
                error_msg = f"{now}: FAG_eval_rpa crashed when trying to type the subject in lectio send message page"
                log.log("FAG_eval_rpa crashed when trying to type the subject in lectio send message page")
                send_sms.sms_troubleshooters(error_msg)
                sys.exit()
            try_attempt = try_attempt + 1

    # checkbox may reply set to unchecked
    try_attempt = 0
    while try_attempt != max_try_attempts:
        try:
            checkbox_may_reply = browser.find_element_by_id("s_m_Content_Content_RepliesToThreadOrExistingMessageAllowedChk")
            if checkbox_may_reply.is_selected():
                checkbox_may_reply.click()
                try_attempt = max_try_attempts
        except NoSuchElementException:
            if try_attempt == max_try_attempts - 1:
                error_msg = f"{now}: FAG_eval_rpa crashed when trying to unclick may reply in lectio send message page"
                log.log("FAG_eval_rpa crashed when trying to unclick may reply in lectio send message page")
                send_sms.sms_troubleshooters(error_msg)
                sys.exit()
            try_attempt = try_attempt + 1

    # insert message in "message field"
    try_attempt = 0
    while try_attempt != max_try_attempts:
        try:
            input_message = browser.find_element_by_id("s_m_Content_Content_CreateThreadEditMessageContent_TbxNAME_tb")
            input_message.send_keys(this_msg)
            try_attempt = max_try_attempts
        except NoSuchElementException:
            if try_attempt == max_try_attempts - 1:
                error_msg = f"{now}: FAG_eval_rpa crashed when trying to type the message in lectio send message page"
                log.log("FAG_eval_rpa crashed when trying to type the message in lectio send message page")
                send_sms.sms_troubleshooters(error_msg)
                sys.exit()
            try_attempt = try_attempt + 1

    # click submit button

    try_attempt = 0
    while try_attempt != max_try_attempts and disbale_send is False:
        try:
            pass
            button_submit = browser.find_element_by_id("s_m_Content_Content_CreateThreadEditMessageOkBtn")
            button_submit.click()
            try_attempt = max_try_attempts
        except NoSuchElementException:
            if try_attempt == max_try_attempts - 1:
                error_msg = f"{now}: FAG_eval_rpa crashed when trying to click the submit button in lectio send message page"
                log.log("FAG_eval_rpa crashed when trying to click the submit button in lectio send message page")
                send_sms.sms_troubleshooters(error_msg)
                sys.exit()
            try_attempt = try_attempt + 1


def get_webpage(this_webpage) -> bs4.BeautifulSoup:
    page = requests.get(this_webpage)
    soup = bs4.BeautifulSoup(page.content, "html.parser")
    return soup

def search_webpage_for_schools(school_name=""): # -> List[str, int]:
    page = get_webpage("https://www.lectio.dk/lectio/login_list.aspx")

    this_list :list = []
    this_dict :dict = {}


    raw_schools = page.find_all('a', href=True)
    for item in raw_schools:
        if "default.aspx" in str(item):
            if school_name in str(item) or school_name == "":
                this_id = get_digits_from_string(str(item))
                this_school = str(item).split(">")[1:]
                this_school = str(this_school)[:-9]
                this_school = this_school[2:]
                this_list.append([('id' , str(this_id)), ('school_name' , this_school)])

    this_dict.update(this_list)
    this_dict = clean_for_json(this_dict)

    json_object = json.dumps(this_dict, indent=4)
    return this_dict

def clean_for_json(this_dict :str) -> str:
    this_dict = str(this_dict).replace("(", '').replace(")", '')
    this_dict = "{'schools': [" + this_dict + "]}"
    this_dict = this_dict.replace("'id'", "{'id")
    this_dict = this_dict.replace("'school_name',", "'school_name' :")
    this_dict = this_dict.replace(",", "}, ")
    this_dict = this_dict.replace(",", "}, ")
    this_dict = this_dict.replace("'id}},", "{'id' :")
    this_dict = this_dict.replace(": 'school_name'", ", 'school_name'")
    this_dict = this_dict.replace("{{", "{")
    this_dict = this_dict.replace("}}", "}")
    this_dict = this_dict.replace("{{", "{")
    this_dict = this_dict.replace("}}", "}")
    #this_dict = this_dict.replace("'", '"')
    return  this_dict

def get_digits_from_string(string :str) -> str:
    digits = ""
    for c in string:
        if c.isdigit():
            digits = digits + c
    return digits

def get_webdriver() -> webdriver:
    browser = webdriver.Chrome(ChromeDriverManager().install())
    return browser

def main():
    lectio_user = config('LECTIO_RPA_USER')
    lectio_password = config('LECTIO_RPA_PASSWORD')
    print(lectio_login(235, lectio_user, lectio_password, get_webdriver()))



if __name__ == "__main__":
    main()


