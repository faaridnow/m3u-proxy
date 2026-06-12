import os
from flask import Flask, redirect
import requests
import re

app = Flask(__name__)

def get_live_m3u8_url():
    try:
        # İTV-nin əsas canlı yayım səhifəsi
        target_url = "https://live.itv.az/" 
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://live.itv.az/'
        }
        
        response = requests.get(target_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # İTV saytındakı həm tam, həm də qısa (/itv.m3u8) linkləri tapmaq üçün xüsusi axtarış
            match = re.search(r'["\'](.*?\.m3u8.*?)["\']', response.text)
            if match:
                found_url = match.group(1).replace('\\', '')
                
                # Əgər link qısadırsa, onu bütöv linkə çeviririk
                if found_url.startswith('/'):
                    return "https://live.itv.az" + found_url
                elif not found_url.startswith('http'):
                    return "https://live.itv.az/" + found_url
                
                return found_url
    except Exception as e:
        print(f"Xəta: {e}")
    
    # Əgər sayt yenilənərsə və ya skript linki tapa bilməsə, birbaşa sənin verdiyin işlək linki qaytarır
    return "https://live.itv.az/itv.m3u8?bandwidth=3900&shift=0"

@app.route('/')
def home():
    return "İTV Server Tam Aktivdir! /kanal.m3u8 istifadə edin."

@app.route('/kanal.m3u8')
def redirectToLiveM3u8():
    return redirect(get_live_m3u8_url(), code=302)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
