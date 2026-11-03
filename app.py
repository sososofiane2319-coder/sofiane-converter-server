from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)
API_KEY = "SOFIANE123"

@app.route("/")
def home():
    return "SOFIANE MPD Server is Running! 24/7"

@app.route("/convert")
def convert():
    m3u_url = request.args.get("url")
    key = request.args.get("key")
    if key != API_KEY:
        return jsonify({"error": "key invalid"}), 403
    if not m3u_url:
        return jsonify({"error": "url missing"}), 400
    # تحويل بسيط M3U8 -> MPD
    mpd_url = m3u_url.replace(".m3u8", ".mpd") if ".m3u8" in m3u_url else m3u_url
    return jsonify({"mpd": mpd_url, "status": "ok"})

@app.route("/extract")
def extract_series():
    page_url = request.args.get("url")
    key = request.args.get("key")
    if key != API_KEY:
        return jsonify({"error": "key invalid"}), 403
    try:
        ydl_opts = {'quiet': True, 'no_warnings': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(page_url, download=False)
            episodes = []
            if 'entries' in info and info['entries']:
                for e in info['entries']:
                    if not e: continue
                    t = e.get('title','حلقة')
                    badge = "مدبلجة" if "مدبلج" in t else "مترجمة" if "مترجم" in t else "عادي"
                    episodes.append({"title": t, "url": e.get('url',''), "type": badge})
            else:
                t = info.get('title','حلقة')
                badge = "مدبلجة" if "مدبلج" in t else "مترجمة" if "مترجم" in t else "عادي"
                episodes.append({"title": t, "url": info.get('url',''), "type": badge})
        return jsonify({"episodes": episodes, "title": info.get('title','مسلسل')})
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)