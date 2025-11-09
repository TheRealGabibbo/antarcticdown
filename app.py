import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from yt_dlp import YoutubeDL
import logging

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

@app.route('/download', methods=['GET'])
def download_video():
    try:
        url = request.args.get('url')
        if not url:
            return jsonify({'error': 'Missing URL'}), 400
        
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'quiet': True,
            'no_warnings': True,
            'socket_timeout': 30,
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            if 'url' not in info:
                return jsonify({'error': 'No downloadable URL found'}), 404
            
            return jsonify({
                'download_url': info['url'],
                'title': info.get('title', 'Unknown'),
                'duration': info.get('duration', 0)
            })
            
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'antarcticdown'})

@app.route('/')
def home():
    return jsonify({
        'service': 'AntarcticDown',
        'status': 'healthy', 
        'version': '1.0',
        'message': 'Video downloader backend is running!',
        'endpoints': {
            'download': '/download?url=YOUTUBE_URL',
            'health': '/health'
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)