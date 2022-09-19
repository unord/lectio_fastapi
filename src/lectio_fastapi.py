from fastapi import FastAPI
from pydantic import BaseModel
from . import lectio
app = FastAPI()


class SendMsg(BaseModel):
    lectio_school_id: int
    lectio_user: str
    lectio_password: str
    send_to: str
    subject: str
    msg: str
    msg_can_be_replied: bool

class SchoolName(BaseModel):
    lectio_school_name: str


@app.get("/")
def read_root():
    return {'msg': 'welcome to the lectio-fastapi', 'success': True}


@app.get("/school_ids/")
def get_school_id(lectio_school_name: str):
    json_object = lectio.lectio_search_webpage_for_schools(lectio_school_name)
    return json_object

@app.post("/school_ids/")
def get_school_id(lectio_school_name: SchoolName):
    #lectio_school_id_results = lectio.lectio_search_webpage_for_schools(lectio_school_name)
    return lectio_school_name


@app.post("/message_send/{lectio_school_id, lectio_user, lectio_password}")
def test_login(lectio_school_id: int, lectio_user: str, lectio_password: str):
    browser = lectio.get_webdriver()
    lectio_login_result = lectio.lectio_login(lectio_school_id, lectio_user, lectio_password, browser)
    return lectio_login_result

@app.get("/message_send/")
def send_msg(lectio_school_id: int, lectio_user: str, lectio_password: str, send_to :str, subject: str, msg: str, msg_can_be_replied: bool):
    browser = lectio.get_webdriver()
    lectio_login_result = lectio.lectio_login(lectio_school_id, lectio_user, lectio_password,browser)
    if lectio_login_result['success']:
        lectio_send_msg_result = lectio.lectio_send_msg(send_to, subject, msg, msg_can_be_replied, lectio_school_id, browser)
        return lectio_send_msg_result
    else:
        return {'msg': 'Login failed, wrong username, password and school_id combination ', 'success': False}

@app.post("/message_send/")
def send_msg(send_msg: SendMsg):
    browser = lectio.get_webdriver()
    lectio_login_result = lectio.lectio_login(send_msg.lectio_school_id, send_msg.lectio_user, send_msg.lectio_password, browser)
    if lectio_login_result['success']:
        lectio_send_msg_result = lectio.lectio_send_msg(send_msg.send_to, send_msg.subject, send_msg.msg, send_msg.msg_can_be_replied, send_msg.lectio_school_id, browser)
        return lectio_send_msg_result
    else:
        return {'msg': 'Login failed, wrong username, password and school_id combination ', 'success': False}

def main():
    pass


if __name__ == "__main__":
    main()