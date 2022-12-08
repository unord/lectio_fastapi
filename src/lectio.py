import time
import requests
import bs4
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import os


def clean_for_json(this_dict: str) -> str:
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
    return this_dict


def get_digits_from_string(string: str) -> str:
    digits = ""
    for c in string:
        if c.isdigit():
            digits = digits + c
    return digits


def get_webdriver() -> webdriver:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
    return browser


def get_webpage(this_webpage) -> bs4.BeautifulSoup:
    page = requests.get(this_webpage)
    soup = bs4.BeautifulSoup(page.content, "html.parser")
    return soup


def lectio_login(school_id: int, lectio_user: str, lectio_password: str, browser: webdriver) -> dict:
    print(f'Logging in to school id: {school_id}')
    max_try_attempts = 100

    this_url = f"https://www.lectio.dk/lectio/{school_id}/login.aspx"

    # go to login page
    try:
        browser.get(this_url)
    except Exception as e:
        return {'msg': f'Could not load page. Exception: {e}', 'success': False}
    print('Username inserted')

    # insert username in lectio login, user field
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

    # insert password in lectio login page, password field
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
    print('Password inserted')
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
    print('Login button clicked')
    time.sleep(1)
    browser.get(f"https://www.lectio.dk/lectio/{school_id}/forside.aspx")
    try:
        current_user = browser.find_element("id", "s_m_LoginOutLink").text
        print(f'Logged in as: {lectio_user}')
        return {'msg': 'Login successful', 'success': True}
    except NoSuchElementException as e:
        print(f'Could not find current user. Exception: {e}')
        return {'msg': f'Login failed, wrong username, password and school_id combination. Exceptiom: {e} ', 'success': False}


def lectio_send_msg(send_to: str, subject: str, msg: str, this_msg_can_be_replied: bool, lectio_school_id: int, browser: webdriver) -> dict:
    max_try_attempts = 100
    main_page_url = f"https://www.lectio.dk/lectio/{lectio_school_id}/forside.aspx"
    print(f'Going to main page: {main_page_url}')
    msg = msg.replace("##n", "\n")
    msg = msg.replace("##ae", "æ")
    msg = msg.replace("##oe", "ø")
    msg = msg.replace("##aa", "å")
    msg = msg.replace("##AE", "Æ")
    msg = msg.replace("##OE", "Ø")
    msg = msg.replace("##AA", "Å")

    # go to main page
    try:
        browser.get(main_page_url)
    except Exception as e:
        print(e)
        return {'msg': 'Could not load page', 'success': False}
    print('Main page loaded')
    # go to lectio new message page
    time.sleep(1)
    try:
        link_beskeder = browser.find_element("xpath", '/html/body/div[1]/form[2]/section/div[2]/div[2]/nav/div/div[12]/a')
        link_beskeder.click()
    except Exception as e:
        print(e)
        return {'msg': 'Could not find link: Beskeder', 'success': False}
    print('Link: "Beskeder" clicked')


    # go to lectio message page
    try:
        link_beskeder = browser.find_element("xpath", '/html/body/div[1]/form[2]/section/div[3]/div/div[3]/div[2]/div[1]/div[1]/a')
        link_beskeder.click()
    except Exception as e:
        return {'msg': f'Could not find link: Ny besked. Exception: {e}', 'success': False}
    print('Message page loaded')
    print('Inserting message')
    # insert class in "to field"
    try_attempt = 0
    while try_attempt != max_try_attempts:
        try:
            input_class_name = browser.find_element("id", "s_m_Content_Content_addRecipientDD_inp")
            input_class_name.send_keys(send_to)
            input_class_name.send_keys(Keys.ARROW_DOWN)
            input_class_name.send_keys(Keys.ARROW_DOWN)
            input_class_name.send_keys(Keys.ENTER)
            try_attempt = max_try_attempts
        except NoSuchElementException:
            if try_attempt == max_try_attempts - 1:
                return {'msg': 'Could not find who to send to. May be problems loading lectio.dk', 'success': False}
            try_attempt += 1
    print('Class inserted')

    '''
    # test to if receiver is correct
    try_attempt = 0
    input_receiver_name = ""
    while try_attempt != max_try_attempts:
        try:
            input_receiver_name = browser.find_element(By.CSS_SELECTOR, "#s_m_Content_Content_CreateThreadEditMessageGV > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > span:nth-child(1)").text
            if input_receiver_name != send_to or input_receiver_name == "":
                return {'msg': f'Value of who is being sent to, is not the same as the receiver found on lectio.dk. User found by lectio.dk: {input_receiver_name}', 'success': False}
            try_attempt = max_try_attempts
        except NoSuchElementException:
            if try_attempt == max_try_attempts - 1:
                return {'msg': 'Could not find who the msg is being sent to. May be problems loading lectio.dk', 'success': False}
            try_attempt += 1

    print('Receiver is correct')
    '''

    # insert message in "subject field"
    try_attempt = 0
    while try_attempt != max_try_attempts:
        try:
            input_subject = browser.find_element("id", "s_m_Content_Content_CreateThreadEditMessageTitle_tb")
            input_subject.send_keys(subject)
            try_attempt = max_try_attempts
        except NoSuchElementException:
            if try_attempt == max_try_attempts - 1:
                return {'msg': 'Could not find who to subject field. May be problems loading lectio.dk', 'success': False}
            try_attempt = try_attempt + 1

    print('Subject inserted')
    # checkbox may reply
    if this_msg_can_be_replied is False:
        try:
            checkbox_may_reply = browser.find_element("id", "s_m_Content_Content_RepliesToThreadOrExistingMessageAllowedChk").click()
        except Exception as e:
            return {'msg': f'Could not find checkbox: may reply. Exception: {e}', 'success': False}

    print('Checkbox may reply processed')
    # insert message in "message field"
    try_attempt = 0
    while try_attempt != max_try_attempts:
        try:
            input_message = browser.find_element("id", "s_m_Content_Content_CreateThreadEditMessageContent_TbxNAME_tb")
            input_message.send_keys(msg)
            try_attempt = max_try_attempts
        except NoSuchElementException:
            if try_attempt == max_try_attempts - 1:
                return {'msg': 'Could not insert message in message field. May be problems loading lectio.dk', 'success': False}
            try_attempt = try_attempt + 1
    print('Message inserted')
    print('Sending message')

    # click submit button
    current_url = browser.current_url
    try_attempt = 0
    while try_attempt != max_try_attempts:
        try:
            pass
            button_submit = browser.find_element("id", "s_m_Content_Content_CreateThreadEditMessageOkBtn")
            button_submit.click()
            try_attempt = max_try_attempts
        except NoSuchElementException:
            if try_attempt == max_try_attempts - 1:
                return {'msg': 'Could not click submit button. May be problems loading lectio.dk', 'success': False}
            try_attempt = try_attempt + 1

    while current_url == browser.current_url:
        print('Waiting for message to be sent')
        time.sleep(1)

    print('Message sent')
    return {'msg': f'message sent successful to: {send_to}', 'success': True}


def lectio_search_webpage_for_schools(school_name="") -> dict:
    page = get_webpage("https://www.lectio.dk/lectio/login_list.aspx")

    this_list: list = []
    this_dict: dict = {}

    raw_schools = page.find_all('a', href=True)
    for item in raw_schools:
        if "default.aspx" in str(item):
            if school_name in str(item) or school_name == "":
                this_id = get_digits_from_string(str(item))
                this_school = str(item).split(">")[1:]
                this_school = str(this_school)[:-9]
                this_school = this_school[2:]
                this_list.append([('id', str(this_id)), ('school_name', this_school)])

    this_dict.update(this_list)
    this_dict = clean_for_json(this_dict)
    return this_dict


def main():
    pass


if __name__ == "__main__":
    main()
