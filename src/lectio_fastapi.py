from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from . import lectio
app = FastAPI()


@app.get("/")
def read_root():
    return {'success': True}

@app.get("/school_ids/{lectio_school_name}")
def get_school_id(lectio_school_name: str):
    json_object = lectio.search_webpage_for_schools(lectio_school_name)
    #json_object = jsonable_encoder(json_object)
    return JSONResponse(content=json_object)

@app.get("/message_send/{lectio_school_id, lectio_user, lectio_password}")
def test_login(lectio_school_id: int, lectio_user: str, lectio_password: str):
    lectio_login_result = lectio.lectio_login(lectio_school_id, lectio_user, lectio_password, lectio.get_webdriver())
    return lectio_login_result

@app.get("/message_send/{lectio_school_id, lectio_user, lectio_password, send_to, subject, msg, msg_can_be_replied}")
def send_msg(lectio_school_id: int, lectio_user: str, lectio_password: str, send_to :str, subject: str, msg: str, msg_can_be_replied: bool):
    browser = lectio.get_webdriver()
    lectio_login_result = lectio.lectio_login(lectio_school_id, lectio_user, lectio_password,browser)
    if lectio_login_result['success']:
        lectio_send_msg_result = lectio.lectio_send_msg(send_to, subject, msg, msg_can_be_replied, lectio_school_id, browser)
        return lectio_send_msg_result
    else:
        return {'success': False}

def main():
    pass

if __name__ == "__main__":
    main()