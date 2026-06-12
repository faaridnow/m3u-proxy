from flask import Flask, Response
import requests
import re

app = Flask(__name__)

def get_live_m3u8_url():
    try:
        # 1. BURA HƏR DƏFƏ GİRDİYİN SAYTIN LİNKİNİ YAZIRSAN
        target_url = "https://www.ornek-site.com/canli-tv-sehifesi" 
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        # Saytın kodunu yükləyirik
        response = requests.get(target_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # 2. Saytın daxilindən ".m3u8" ilə bitən real yayım linkini tapırıq
            match = re.search(r'(https?://[^\s"\']+\.m3u8[^\s"\']*)', response.text)
            
            if match:
                # Tapılan linki təmizləyib geri qaytarır
                cleaned_url = match.group(1).replace('\\', '')
                return cleaned_url
    except Exception as e:
        print(f"Səhv baş verdi: {e}")
    
    # Əgər sayt çöksə və ya link tapılmasa, bura müvəqqəti bir işlək link qoya bilərsən
    return "https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.ism/.m3u8"

@app.route('/kanal.m3u')
def generate_m3u():
    # Saytdan ən son yenilənmiş .m3u8 linkini çəkirik
    live_stream_url = get_live_m3u8_url()
    
    # IPTV Pleyerin oxuya biləcəyi M3U formatını hazırlayırıq
    m3u_content = f"""#EXTM3U
#EXTINF:-1 tvg-id="Kanal1" tvg-name="Canlı Kanal" tvg-logo="" group-title="Kanallar",Canlı Kanal
{live_stream_url}
"""
    return Response(m3u_content, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
