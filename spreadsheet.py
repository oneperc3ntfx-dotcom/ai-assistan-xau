import gspread
from google.oauth2.service_account import Credentials


SPREADSHEET_ID = "1J3_Go0MdiNaDxVl6EuA00hJMsamB35Gjq0eHEg96ZMw"
SHEET_NAME = "Members"


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


# koneksi Google Sheet
creds = Credentials.from_service_account_file(
    "service_account.json",
    scopes=SCOPES
)

client = gspread.authorize(creds)

sheet = client.open_by_key(
    SPREADSHEET_ID
).worksheet(
    SHEET_NAME
)



def save_member(data):

    try:

        print("=== DATA KE SPREADSHEET ===")
        print(data)


        sheet.append_row([

            data.get("telegram_id", ""),

            data.get("username", ""),

            data.get("nama", ""),

            data.get("paket", ""),

            data.get("harga", ""),

            data.get("register", ""),

            data.get("expired", ""),

            data.get("status", "")

        ])


        print("STATUS:")
        print("SUCCESS")


        print("RESPON GOOGLE SHEET:")
        print("Member berhasil disimpan")


        return True


    except Exception as e:

        print(
            "Google Sheet Error:",
            e
        )

        return False
