from flask import Flask
import platform

app = Flask(__name__)

@app.route('/')
def hello():
    return {
        "message": "Hello world!"
    }

@app.route('/system')
def system_info():
    return {
        'Platform': platform.platform(),
        'Node': platform.node(),
    }

if __name__ == '__main__':
    app.run(host="0.0.0.0")