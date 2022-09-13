from typing import Union
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"lectio_school_id": "int", }


@app.get("/message_send/{lectio_school_id, lectio_user, lectio_password, lectio_subject, lectio_msg, lectio_can_answer, lectio_test}")
def send_msg(lectio_school_id: int, lectio_user: str, lectio_password: str, lectio_subject: str, lectio_msg: str, lectio_can_answer: bool, lectio_test: bool):
    return {"lectio_school_id": lectio_school_id}

@app.get("/message_send/{lectio_school_id, lectio_user, lectio_password}")
def test_login(lectio_school_id: int, lectio_user: str, lectio_password: str):
    login_successful = False
    return {"login_successful": login_successful}

@app.get("/school_ids/{lectio_school_id, lectio_school_name}")
def test_login(lectio_school_id: int, lectio_school_name: str):
    school_list = {}
    return school_list

def main():
    pass

if __name__ == "__main__":
    main()