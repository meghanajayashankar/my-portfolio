from flask import Flask, request
import csv
import os

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def handle_form():
    try:
        user_data = {
            'Name': request.form.get('name'),
            'Email': request.form.get('email'),
            'Message': request.form.get('message')
        }
        
        file_exists = os.path.isfile('database.csv')
        with open('database.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Name', 'Email', 'Message'])
            if not file_exists: writer.writeheader()
            writer.writerow(user_data)

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