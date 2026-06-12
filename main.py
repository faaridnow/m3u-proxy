import os
from flask import Flask, Response, redirect
import requests
import re

app = Flask(__name__)

def get_live_m3u8_url():
    try:
        # Bura öz əsas saytının linkini yazırsan
        target_url = "https://live.itv.az/" 
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(target_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            match = re.search(r'(https?://[^\s"\']+\.m3u8[^\s"\']*)', response.text)
            if match:
                return match.group(1).replace('\\', '')
    except Exception as e:
        print(f"Xəta: {e}")
    
    return "https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.ism/.m3u8"

@app.route('/')
def home():
    return "Server Tam Aktivdir! /kanal.m3u8 istifadə edin."

@app.route('/kanal.m3u8')
def redirectToLiveM3u8():
    return redirect(get_live_m3u8_url(), code=302)

if __name__ == '__main__':
    # Render üçün vacib olan dinamik port ayarı
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
