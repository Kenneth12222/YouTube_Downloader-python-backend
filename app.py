# app.py
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from pytube import YouTube
import os
import tempfile

app = Flask(__name__)
CORS(app) 

@app.route('/download', methods=['GET'])
def download_video():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()

        temp_file = tempfile.NamedTemporaryFile(delete=False)
        stream.download(output_path=os.path.dirname(temp_file.name), filename=os.path.basename(temp_file.name))

        return send_file(temp_file.name, as_attachment=True, download_name='video.mp4', mimetype='video/mp4')


    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080)
