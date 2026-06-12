import os
from flask import Flask, Response
import requests
import re

app = Flask(__name__)

def get_live_m3u8_url():
    try:
        target_url = "https://live.itv.az/" 
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://live.itv.az/'
        }
        response = requests.get(target_url, headers=headers, timeout=10)
        if response.status_code == 200:
            match = re.search(r'["\'](.*?\.m3u8.*?)["\']', response.text)
            if match:
                found_url = match.group(1).replace('\\', '')
                if found_url.startswith('/'):
                    return "https://live.itv.az" + found_url
                elif not found_url.startswith('http'):
                    return "https://live.itv.az/" + found_url
                return found_url
    except Exception as e:
        print(f"Xəta: {e}")
    
    return "https://live.itv.az/itv.m3u8?bandwidth=3900&shift=0"

@app.route('/')
def home():
    return "İTV Server Tam Aktivdir!"

# YENİ PROXY METODU (Yönləndirməsiz birbaşa yayım)
@app.route('/kanal.m3u8')
def proxy_m3u8():
    real_url = get_live_m3u8_url()
    try:
        # İTV-nin yayımını bizim server arxa fonda çəkir
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        res = requests.get(real_url, headers=headers, stream=True, timeout=10)
        
        # İçindəki mətni SSIPTV-yə olduğu kimi canlı ötürürük
        return Response(res.text, mimetype='application/x-mpegURL')
    except Exception as e:
        return f"Yayım çəkilə bilmədi: {e}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
