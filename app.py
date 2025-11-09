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
        
        # CONFIGURAZIONE SEMPLICE E FUNZIONANTE
        ydl_opts = {
            'format': 'best',
            'quiet': True,
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # VERIFICA che sia un URL video vero
            video_url = info['url']
            if 'googlevideo.com' not in video_url:
                return jsonify({'error': 'Invalid video URL extracted'}), 500
            
            return jsonify({
                'download_url': video_url,
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
        'version': '1.0'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)