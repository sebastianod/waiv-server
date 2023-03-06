# Import flask and datetime module for showing date and time
from flask import Flask
from flask_cors import CORS
import datetime

# Initializing flask app
app = Flask(__name__)

#enable CORS
CORS(app)

# Route for seeing a data
@app.route('/data', methods=['GET','POST'])
def get_data():
    x = datetime.datetime.now()
    # Returning an api for showing in reactjs
    return {
        'Name': 'geek', 
        'Age': '22',
        'Date': x.strftime('%Y-%m-%d %H:%M:%S'), 
        'Programming': 'python'
    }

# Running app
if __name__ == '__main__':
    app.run(debug=True)