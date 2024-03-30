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
    if 'toLang' in data['payload']:
        to_lang = data['payload']['toLang']

    print(f"from_lang: {from_lang}, to_lang: {to_lang}")

    # Extract text and id from records
    texts = [record.get('text', '') for record in text_records if record.get('text')]
    ids = [record.get('id') for record in text_records]

    # Batch translate the texts
    translated_texts = translator.batch(texts, src_lang=from_lang, tgt_lang=to_lang)

    # Ensure alignment of IDs and translated texts
    translated_records = [{'id': _id or utils.md5(text), 'text': translated_text}
                          for _id, text, translated_text in zip(ids, texts, translated_texts)]

    return jsonify({
        'status': 'success',
        'code': 200,
        'result': translated_records
    })


def translate(texts: list[str], from_lang: str, to_lang: str):
    """Translate the text to the target language function with batch."""
    translated_text = translator.batch(texts, from_lang, to_lang)
    return translated_text


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9527)

