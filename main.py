#AI powerd word suggestion
import os
from flask import Flask,jsonify
from flask_cors import cross_origin

from utils import (
        generate_appended_strings,
        generate_prepended_strings,
        generate_tlds,
        merge_words,
        generate_top_10,
)

from aws_utils import download_from_s3

app = Flask(__name__)

S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
KEY_NAME = os.getenv('KEY_NAME')
DOWNLOAD_FILE_NAME = os.getenv('DOWNLOAD_FILE_NAME')

if not os.path.exists(DOWNLOAD_FILE_NAME):
    download_from_s3(S3_BUCKET_NAME,KEY_NAME,DOWNLOAD_FILE_NAME)

@app.route('/',methods=["GET","OPTIONS"])
@cross_origin()
def index():
    return jsonify({'message': 'Server is running'})


@app.route('/merge/<string:word1>/<string:word2>',methods=["GET","OPTIONS"])
@cross_origin()
def generate_merge_words(word1,word2):
    return jsonify({"suggestions_for_two_words": merge_words(word1,word2)})


@app.route("/generate/<string:word>",methods=["GET","OPTIONS"])
@cross_origin()
def generate_all(word):
    generators = {
                    'append': generate_appended_strings,
                    'prepend': generate_prepended_strings,
                    'tlds': generate_tlds,
                    "ai_powered_word_score": generate_top_10
                }
    result = {}
    for op,fn in generators.items(): 
            result[op] = fn(word)
    return jsonify(result)
    
if __name__ == '__main__':
    
    port = os.getenv('PORT',None) or 80
    app.run(host='0.0.0.0',port=port)
