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
    return "İTV Server Tam Aktivdir!"

@app.route('/kanal.m3u8')
def proxy_m3u8():
    real_url = get_live_m3u8_url()
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Referer': 'https://live.itv.az/'
        }
        res = requests.get(real_url, headers=headers, timeout=10)
        
        if res.status_code == 200:
            lines = res.text.splitlines()
            rewritten_lines = []
            base_url = "https://live.itv.az/"
            
            for line in lines:
                line = line.strip()
                if line:
                    # Faylın içindəki qısa linkləri bütöv İTV linkinə çeviririk
                    if not line.startswith('#') and not line.startswith('http'):
                        if line.startswith('/'):
                            line = "https://live.itv.az" + line
                        else:
                            line = base_url + line
                    # Teqlərin daxilində gizlənən digər keçidləri düzəldirik
                    elif line.startswith('#') and 'URI=' in line:
                        line = line.replace('URI="', 'URI="https://live.itv.az/')
                        line = line.replace('URI=\'', 'URI=\'https://live.itv.az/')
                rewritten_lines.append(line)
            
            output = "\n".join(rewritten_lines)
            
            # Smart TV-lər (LG/Samsung) üçün CORS icazə başlıqlarını əlavə edirik
            response = Response(output, mimetype='application/x-mpegURL')
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
    except Exception as e:
        print(f"Proxy xətası: {e}")
    
    return "Yayım tapılmadı", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
