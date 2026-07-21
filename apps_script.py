import requests

from config import APPSCRIPT_URL



def save_member(data):

    try:

        print("=== DATA KE SPREADSHEET ===")
        print(data)


        response = requests.post(

            APPSCRIPT_URL,

            json=data,

            timeout=15

        )


        print("STATUS:")
        print(response.status_code)


        print("RESPON APPS SCRIPT:")
        print(response.text)



        return response.text



    except Exception as e:

        print(
            "Apps Script Error:",
            e
        )

        return None
