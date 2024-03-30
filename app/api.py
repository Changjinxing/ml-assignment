# Description: This is the main file for the translation service.
# It uses the Translator class from translator.py to translate text from one language to another.

from flask import Flask, request, jsonify

import utils
from translator import Translator

app = Flask(__name__)

translator = Translator()
translator.load_model()


@app.route('/health_check', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'OK'})


def validate_request_payload(data):
    """Validate the request payload."""
    if 'payload' not in data:
        return False, {'status': 'fail', 'code': 501, 'msg': 'payload field is required'}

    payload = data['payload']
    if 'records' not in payload:
        return False, {'status': 'fail', 'code': 502, 'msg': 'records field is required'}

    return True, None


@app.route('/translation', methods=['POST'])
def translate_text():
    """Translate the text to the target language interface."""

    data = request.json

    # Validate the request payload
    is_valid, validation_error = validate_request_payload(data)
    if not is_valid:
        return jsonify(validation_error)

    text_records = data['payload']['records']
    from_lang = 'en'
    if 'fromLang' in data['payload']:
        from_lang = data['payload']['fromLang']
    to_lang = 'ja'
    if 'toLang' not in data['payload']:
        to_lang = data['payload']['toLang']

    translated_records = []
    for record in text_records:
        text = record.get('text', '')
        if not text:
            continue
        _id = record.get('id', None)
        if not _id:
            _id = utils.md5(text)

        translated_text = translate(text, from_lang, to_lang)
        translated_records.append({'id': _id, 'text': translated_text})

    return jsonify({
        'status': 'success',
        'code': 200,
        'result': translated_records
    })


def translate(text, from_lang, to_lang):
    """Translate the text to the target language function."""
    translated_text = translator.translate(text, from_lang, to_lang)
    return translated_text


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9527)

