from flask import Flask, render_template
import time
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/updates')
def updates():
    def generate_data():
        while True:
            with open(web_file, 'r') as file:
                data = file.read()
            time.sleep(180)  # Wait for 3 minutes
            yield 'data: {}\n\n'.format(data)

    return app.response_class(generate_data(), mimetype='text/event-stream')

if __name__ == '__main__':
    parent_dir = os.path.dirname(os.getcwd())
    web_file = os.path.join(parent_dir, 'BB_signals.txt')
    app.run(host='0.0.0.0', debug=True)
