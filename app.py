from flask import Flask, jsonify, request, render_template, Response

from src.parse import process, normalize_text

app = Flask(__name__)

@app.route('/common_words', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/update', methods=['POST'])
def update():
    res = request.get_json()
    text, words, text_covr, words_covr = process(res['text'], res['words'])

    res = {
        'text': text,
        'words': words,
        'text_covr': text_covr,
        'words_covr': words_covr,
    }
    
    # print(res)

    return jsonify(res)

@app.route('/normalize', methods=['POST'])
def normalize():
    # print(request.get_json())
    res = normalize_text(request.get_json())
    # print(res)
    return jsonify(res)

if __name__ == '__main__':
    app.run(ssl_context='adhoc', template_folder='templates')

# text = 'У попа была собака, он её любил. Она съела кусок мяса - он её убил, в землю закопал и на камне написал: "У попа была собака ..."'
# print(normalize_text(text))