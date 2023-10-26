from decouple import config
import time
import requests
import bs4
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
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

def clean_string_for_json_replace_dk(this_string: str) -> str:
    this_string = this_string.replace("##n", "\n")
    this_string = this_string.replace("##ae", "æ")
    this_string = this_string.replace("##oe", "ø")
    this_string = this_string.replace("##aa", "å")
    this_string = this_string.replace("##AE", "Æ")
    this_string = this_string.replace("##OE", "Ø")
    this_string = this_string.replace("##AA", "Å")
    return this_string


def get_digits_from_string(string: str) -> str:
    digits = ""
    for c in string:
        if c.isdigit():
            digits = digits + c
    return digits


def get_webdriver() -> webdriver:
    chrome_options = webdriver.ChromeOptions() #
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_SHIM", None)
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(service=Service(os.environ.get("CHROMEDRIVER_PATH")), options=chrome_options)
    return browser

def get_webdriver_local() -> webdriver:
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    return driver


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
        current_user = browser.find_element(By.CLASS_NAME, "ls-user-name").text
        print(f'Logged in as: {current_user}')
        return {'msg': 'Login successful', 'success': True}
    except NoSuchElementException as e:
        print(f'Could not find current user. Exception: {e}')
        return {'msg': f'Login failed, wrong username, password and school_id combination. Exceptiom: {e} ', 'success': False}


def lectio_send_msg(send_to: str, subject: str, msg: str, this_msg_can_be_replied: bool, lectio_school_id: int, browser: webdriver) -> dict:
    max_try_attempts = 50
    main_page_url = f"https://www.lectio.dk/lectio/{lectio_school_id}/forside.aspx"
    print(f'Going to main page: {main_page_url}')

    send_to = clean_string_for_json_replace_dk(send_to)
    msg = clean_string_for_json_replace_dk(msg)
    subject = clean_string_for_json_replace_dk(subject)

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
        link_beskeder = browser.find_element(By.PARTIAL_LINK_TEXT, 'Beskeder')
        link_beskeder.click()
    except Exception as e:
        print(e)
        return {'msg': 'Could not find link: Beskeder', 'success': False}
    print('Link: "Beskeder" clicked')


    # go to lectio message page
    try_attempt = 0
    while try_attempt != max_try_attempts:
        try:
            element = browser.find_element(By.ID, 's_m_Content_Content_NewMessageLnk')
            browser.execute_script("arguments[0].click();", element)
            #wait = WebDriverWait(browser, 10)
            #wait.until(EC.visibility_of_element_located((By.ID, "s_m_Content_Content_NewMessageLnk")))
            #link_beskeder = browser.find_element(By.ID, 's_m_Content_Content_NewMessageLnk')
            #link_beskeder = browser.find_element(By.PARTIAL_LINK_TEXT, 'Ny besked')
            #ActionChains(browser).move_to_element(link_beskeder).click(link_beskeder).perform()
            try_attempt = max_try_attempts
        except Exception as e:
            if try_attempt == max_try_attempts - 1:
                print(f"Could not find who to send to. May be problems loading lectio.dk. Current url: {browser.current_url} . Exception: {e}")
                return {'msg': f'Could not find link: Ny besked. Exception: {e}', 'success': False, 'current_url': browser.current_url}
            try_attempt += 1


    print('Message page loaded')
    print('Inserting message')
    # insert class in "to field"
    try_attempt = 0
    while try_attempt != max_try_attempts:
        try:
            input_class_name = browser.find_element(By.ID, "s_m_Content_Content_MessageThreadCtrl_addRecipientDD_inp")
            input_class_name.send_keys(send_to)
            time.sleep(1)
            list_element = browser.find_element(By.XPATH, f"//li[contains(text(),'{send_to} (')]")
            list_element.click()
            #input_class_name.send_keys(Keys.ENTER)
            try_attempt = max_try_attempts
        except NoSuchElementException as e:
            if try_attempt == max_try_attempts - 1:
                print(f"Could not find who to send to. May be problems loading lectio.dk. Exception: {e}")
                return {'msg': 'Could not find who to send to. May be problems loading lectio.dk', 'success': False}
            try_attempt += 1
    print(f'Class inserted. Class: {send_to}')



    # insert message in "subject field"!
    try_attempt = 0
    while try_attempt != max_try_attempts:
        try:
            input_subject = browser.find_element(By.ID, "s_m_Content_Content_MessageThreadCtrl_MessagesGV_ctl02_EditModeHeaderTitleTB_tb")
            input_subject.send_keys(subject)
            try_attempt = max_try_attempts
        except NoSuchElementException as e:
            if try_attempt == max_try_attempts - 1:
                print(f"Could not find who to subject field. exception: {e}")
                return {'msg': 'Could not find who to subject field. May be problems loading lectio.dk', 'success': False}
            try_attempt = try_attempt + 1

    print(f'Subject inserted. Subject: {subject}')
    # checkbox may reply
    if this_msg_can_be_replied is False:
        try:
            browser.find_element(By.ID, "s_m_Content_Content_MessageThreadCtrl_RepliesNotAllowedChkBox").click()
        except Exception as e:
            print(f"Could not find checkbox: may reply. exception: {e}")
            return {'msg': f'Could not find checkbox: may reply. Exception: {e}', 'success': False}

    print('Checkbox may reply processed')
    # insert message in "message field"
    try_attempt = 0
    while try_attempt != max_try_attempts:
        try:
            input_message = browser.find_element(By.ID, "s_m_Content_Content_MessageThreadCtrl_MessagesGV_ctl02_EditModeContentBBTB_TbxNAME_tb")
            input_message.send_keys(msg)
            try_attempt = max_try_attempts
        except NoSuchElementException as e:
            if try_attempt == max_try_attempts - 1:
                print(f"Could not insert message in message field. May be problems loading lectio.dk. exception: {e}")
                return {'msg': 'Could not insert message in message field. May be problems loading lectio.dk', 'success': False}
            try_attempt = try_attempt + 1
    print(f'Message inserted. Message: {msg}')
    print('Sending message')

    # click submit button
    current_url = browser.current_url
    try_attempt = 0
    while try_attempt != max_try_attempts:
        try:
            button_submit = browser.find_element(By.ID, "s_m_Content_Content_MessageThreadCtrl_MessagesGV_ctl02_SendMessageBtn")
            button_submit.click()
            try_attempt = max_try_attempts
            print('Submit button clicked')
            time.sleep(6)
        except NoSuchElementException as e:
            if try_attempt == max_try_attempts - 1:
                print(f"Could not click submit button. May be problems loading lectio.dk. exception: {e}")
                return {'msg': 'Could not click submit button. May be problems loading lectio.dk', 'success': False}
            try_attempt = try_attempt + 1

    print(f'Message sent to: {send_to}')
    print('****************************************************************************************')
    return {'msg': f'message sent successful to: {send_to}', 'success': True}


def download_teacher_information(lectio_school_id: int, browser: webdriver) -> dict:


    browser.get('https://www.lectio.dk/lectio/234/stamdata/stamdata_chooseentity.aspx?type=editteacher')
    time.sleep(1)
    # with selenium download file
    try:
        browser.find_element(By.ID, "m_Content_BtnExportLaerer").click()
    except Exception as e:
        return {'msg': f'Could not find download link. Exception: {e}', 'success': False}



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
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    lectio_login(config("LECTIO_RPA_SCHOOL_ID"), config("LECTIO_RPA_USER"), config("LECTIO_RPA_PASSWORD"), driver)
    time.sleep(5)
    try:
        lectio_send_msg("cbht1b-infc", "test", "test", "234", "234", driver)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
