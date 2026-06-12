import os
from flask import Flask, Response
import requests
import re

app = Flask(__name__)

def get_live_m3u8_url():
    try:
        target_url = "https://live.itv.az/" 
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
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
    return "Server Aktivdir! Pleyerə /playlist.m3u linkini əlavə edin."

# YENİ METOD: Dinamik Pleylist Yaradıcısı
@app.route('/playlist.m3u')
def generate_playlist():
    # Arxa fonda gedib ən təzə linki tapır
    real_url = get_live_m3u8_url()
    
    # Pleyerlərin (SSIPTV, VLC) 100% tanıdığı siyahı formatını hazırlayır
    m3u_content = f"""#EXTM3U
#EXTINF:-1 tvg-id="itv" tvg-name="İTV" group-title="Azərbaycan", İctimai TV
{real_url}
"""
    
    # Siyahını pleyerə mətn faylı kimi təhvil verir
    return Response(m3u_content, mimetype='audio/x-mpegurl')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
