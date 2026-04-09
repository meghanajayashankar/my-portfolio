from flask import Flask, request
import gspread
from google.oauth2.service_account import Credentials
import os

app = Flask(__name__)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open("My Portfolio").sheet1

if sheet.row_count == 0 or sheet.row_values(1) == []:
    sheet.append_row(["Name", "Email", "Message"])


@app.route('/submit', methods=['POST'])
def handle_form():
    try:
        user_data = {
            'Name': request.form.get('name'),
            'Email': request.form.get('email'),
            'Message': request.form.get('message')
        }

        sheet.append_row([user_data['Name'], user_data['Email'], user_data['Message']])

        return """
        <body style="background-color: #12100e; color: white; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; font-family: sans-serif;">
            <h1 style="color: #ff7e5f;">Success!</h1>
            <p>We'll get back to you soon.</p>
            <p>Redirecting you back to the portfolio</p>
            <script>
                setTimeout(function(){
                    window.history.back();
                }, 2000);
            </script>
            <noscript>
                <p>If you aren't redirected, <a href="javascript:history.back()" style="color: #ff7e5f;">click here to go back</a>.</p>
            </noscript>
        </body>
        """
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
