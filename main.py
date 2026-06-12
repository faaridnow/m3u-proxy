from flask import Flask, Response
import requests
import re

app = Flask(__name__)

def get_live_m3u_url():
    try:
        # 1. BURA LİNKİN OLDUĞU SAYTIN ADRESİNİ YAZIRSAN
        target_url = "https://live.itv.az/" 
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(target_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # 2. SAYTIN KODUNDAN M3U8 LİNKİNİ TAPMAQ ÜÇÜN REGEX
            # Bu hissə saytın strukturuna görə dəyişə bilər. 
            # Aşağıdakı kod saytın içindəki "http...m3u8" formatlı linkləri axtarır.
            match = re.search(r'(https?://[^\s"\']+\.m3u8[^\s"\']*)', response.text)
            
            if match:
                return match.group(1)
    except Exception as e:
        print(f"Xəta baş verdi: {e}")
    
    # Əgər saytdan nəsə tapa bilməsə, ehtiyat olmaq üçün köhnə və ya sabit link qoya bilərsən
    return "https://ehtiyat-link.com/live.m3u8"

@app.route('/kanal.m3u')
def generate_m3u():
    # Yenilənmiş dinamik linki saytdan çəkirik
    live_stream_url = get_live_m3u_url()
    
    # IPTV Pleyerinin başa düşəcəyi M3U formatı formatlaşdırırıq
    m3u_content = f"""#EXTM3U
#EXTINF:-1 tvg-id="1Kanal" tvg-name="1 Kanal" tvg-logo="" group-title="Kanallar",1 Kanal
{live_stream_url}
"""
    return Response(m3u_content, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
