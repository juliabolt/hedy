import hedy
import json

# app.py
from flask import Flask, request, jsonify
from flask_compress import Compress

app = Flask(__name__, static_url_path='')
Compress(app)

@app.route('/levels-text/', methods=['GET'])
def levels():
    level = request.args.get("level", None)

    #read levels from file
    try:
        file = open("levels-text.json", "r")
        contents = str(file.read())
        response = (json.loads(contents))
        file.close()
    except Exception as E:
            print(f"error opening level {level}")
            response["Error"] = str(E)
    return jsonify(response)


@app.route('/parse/', methods=['GET'])
def parse():
    # Retrieve the name from url parameter
    lines = request.args.get("code", None)
    level = request.args.get("level", None)

    # For debugging
    print(f"got code {lines}")

    response = {}

    # Check if user sent code
    if not lines:
        response["Error"] = "no code found, please send code."
    # is so, parse
    else:
        try:
            result = hedy.transpile(lines, level)
            response["Code"] = result
        except Exception as E:
            print(f"error transpiling {lines}")
            response["Error"] = str(E)

    return jsonify(response)



# @app.route('/post/', methods=['POST'])
# for now we do not need a post but I am leaving it in for a potential future

# routing to index.html
@app.route('/', methods=['GET'])
def index():
    level = request.args.get("level", None)
    print(level)
    if level == None or level == '1':
        return open("static/index.html").read()
    elif level == '2':
        return open("static/index-2.html").read()



if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
