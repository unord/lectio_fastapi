# lectio_fastapi
fastapi that can retrieve and make actions in lectio.dk


## Usage
The api is running on heroku at https://lectio-fastapi.herokuapp.com 

Documentation is available at https://lectio-fastapi.herokuapp.com/docs#


## Use POST methode to retrieve data
### Example in Python3
```python
import requests
from requests.structures import CaseInsensitiveDict

API_ENDPOINT = "https://lectio-fastapi.herokuapp.com/" #link to fastapi

def lectio_send_msg(lectio_school_id: int, lectio_user: str, lectio_password: str, send_to :str, subject: str, msg: str, msg_can_be_replied: bool):
    url = API_ENDPOINT+"message_send/"
    print(url)

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Content-Type"] = "application/json"

    payload = '{"lectio_school_id": "' + str(lectio_school_id)
    payload = payload + '", "lectio_user": "' + lectio_user
    payload = payload + '", "lectio_password": "' + lectio_password
    payload = payload + '", "send_to": "' + send_to
    payload = payload + '", "subject": "' + subject
    payload = payload + '", "msg": "' + msg
    payload = payload + '", "msg_can_be_replied": "' + str(msg_can_be_replied) + '"}'

    resp_post = requests.post(url, data=payload, headers=headers)
    return resp_post

def main():
    lectio_school_id = 235
    lectio_user = 'test_user'
    lectio_password = 'test_password'
    send_to = 'Mr test'
    subject = 'test subject'
    msg = 'test msg'
    msg_can_be_replied = False
    print(lectio_send_msg(lectio_school_id, lectio_user, lectio_password, send_to, subject, msg, msg_can_be_replied).text)



if __name__ == '__main__':
    main()



````

