import os
from flask import Flask, request, jsonify

PORT = os.getenv('PORT', '5040')

app = Flask(__name__)

@app.route('/')
def index():
    args = dict(request.args)
    environ = dict(os.environ)
    r = request
    return jsonify({'host_url': r.host_url, 'args': args, 'environ': environ})

@app.route('/build')
def build():
    return app.send_static_file('build.txt')

print("Environment Variables:")
for key in os.environ.keys():
    print("%s - %s" %  (key, os.environ[key]))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(PORT))