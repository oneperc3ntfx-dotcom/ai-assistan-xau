import requests

from config import APPSCRIPT_URL



def save_member(data):

    try:

        response = requests.post(
            APPSCRIPT_URL,
            json=data,
            timeout=10
        )


        return response.json()


    except Exception as e:

        print(
            "Apps Script Error:",
            e
        )

        return None
