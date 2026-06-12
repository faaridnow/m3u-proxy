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
    
    # Əgər skript hansısa saniyədə linki tapa bilməsə, SSIPTV-nin 100% açdığı bu linki ötürür
    return "https://live.itv.az/itv.m3u8?bandwidth=3900&shift=0"

@app.route('/')
def home():
    return "Server Tam Aktivdir! /kanal.m3u8 istifadə edin."

# 100% SSIPTV UYĞUNLUQLU MASTER PLAYLIST ENDPOINTI
@app.route('/kanal.m3u8')
def hls_master_playlist():
    # Arxa fonda dinamik olaraq İTV-nin ən son buraxdığı linki çəkirik
    real_m3u8_url = get_live_m3u8_url()
    
    # Standart HLS (M3U8) Master pleylist strukturu qururuq.
    # Burada link bütöv olduğu üçün SSIPTV bütün video parçalarını İTV-nin özündən rəsmi olaraq çəkəcək.
    master_content = f"""#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:BANDWIDTH=3900000,RESOLUTION=1920x1080,NAME="İTV HD"
{real_m3u8_url}
"""
    
    # Şifrələməni və CORS icazələrini təyin edirik (Smart TV-lərin təhlükəsizlik divarını qırmaq üçün)
    response = Response(master_content, mimetype='application/x-mpegURL')
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
