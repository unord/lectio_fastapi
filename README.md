# lectio_fastapi
fastapi that can retrieve and make actions in lectio.dk


## Usage
The api is running on heroku at https://lectio-fastapi.herokuapp.com 

Documentation is available at https://lectio-fastapi.herokuapp.com/docs#


## Use POST methode to retrieve data
### Example for Python3
```python
import requests
import json  # Import the json module

API_ENDPOINT = "https://lectio-fastapi.herokuapp.com/"  # Link to api

def lectio_send_msg(lectio_school_id, lectio_user, lectio_password, send_to, subject, msg, msg_can_be_replied):
    url = f"{API_ENDPOINT}message_send/"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # Use Python's json.dumps to convert the dictionary to a JSON string
    payload = json.dumps({
        "lectio_school_id": lectio_school_id,
        "lectio_user": lectio_user,
        "lectio_password": lectio_password,
        "send_to": send_to,
        "subject": subject,
        "msg": msg,
        "msg_can_be_replied": msg_can_be_replied
    })

    resp_post = requests.post(url, json=payload, headers=headers)

    # Explicitly set the encoding to UTF-8 if needed (usually, requests will handle this)
    resp_post.encoding = 'utf-8'

    return resp_post.text  # Text content should now be properly UTF-8 encoded/decoded

def main():
    lectio_school_id = 235
    lectio_user = 'test_user'
    lectio_password = 'test_password'
    send_to = 'Mr test'
    subject = 'test subject'
    msg = 'test msg'
    msg_can_be_replied = False
    print(lectio_send_msg(lectio_school_id, lectio_user, lectio_password, send_to, subject, msg, msg_can_be_replied))

if __name__ == '__main__':
    main()

````

