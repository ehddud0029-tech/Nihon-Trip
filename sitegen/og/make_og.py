# 공유 미리보기 이미지(og-<lang>.png, 1200x630) 생성: python3 sitegen/og/make_og.py
import os
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__))
T = {
 "ko": ("일본 여행, 지역별로 한눈에", "도쿄 · 오사카 · 후쿠오카 · 홋카이도 · 오키나와 · 나고야 · 히로시마 · 시코쿠", "볼거리 · 맛집 · 쇼핑 · 축제 · 추천 일정", "Noto Sans CJK KR"),
 "en": ("Japan travel, region by region", "Tokyo · Osaka · Fukuoka · Hokkaido · Okinawa · Nagoya · Hiroshima · Shikoku", "Sights · Food · Shopping · Festivals · Itineraries", "Noto Sans CJK JP"),
 "ja": ("日本旅行を、エリアごとに", "東京 · 大阪 · 福岡 · 北海道 · 沖縄 · 名古屋 · 広島 · 四国", "観光 · グルメ · ショッピング · 祭り · モデルコース", "Noto Sans CJK JP"),
 "zh": ("日本旅行，按地区一目了然", "东京 · 大阪 · 福冈 · 北海道 · 冲绳 · 名古屋 · 广岛 · 四国", "景点 · 美食 · 购物 · 节庆 · 推荐行程", "Noto Sans CJK SC"),
 "tw": ("日本旅行，依地區一目了然", "東京 · 大阪 · 福岡 · 北海道 · 沖繩 · 名古屋 · 廣島 · 四國", "景點 · 美食 · 購物 · 節慶 · 推薦行程", "Noto Sans CJK TC"),
 "es": ("Japón, región por región", "Tokio · Osaka · Fukuoka · Hokkaido · Okinawa · Nagoya · Hiroshima · Shikoku", "Lugares · Comida · Compras · Festivales · Itinerarios", "Noto Sans CJK JP"),
 "fr": ("Le Japon, région par région", "Tokyo · Osaka · Fukuoka · Hokkaido · Okinawa · Nagoya · Hiroshima · Shikoku", "Sites · Cuisine · Shopping · Fêtes · Itinéraires", "Noto Sans CJK JP"),
}
HTML = """<html><body style="margin:0"><div style="width:1200px;height:630px;box-sizing:border-box;background:#F4F5F1;
font-family:'{f}';color:#1C2433;position:relative;overflow:hidden;padding:84px 90px">
<div style="position:absolute;right:-120px;top:-120px;width:520px;height:520px;border-radius:50%;background:#C4452C;opacity:.10"></div>
<div style="position:absolute;left:0;bottom:0;width:100%;height:14px;background:#23395B"></div>
<div style="display:flex;align-items:center;gap:30px">
 <div style="width:132px;height:132px;border-radius:22px;background:#C4452C;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:62px;letter-spacing:1px">GO</div>
 <div><div style="font-size:78px;font-weight:900;line-height:1">Go Nihon Trip</div>
 <div style="font-size:28px;color:#5A6272;margin-top:12px;letter-spacing:1px">gonihontrip.com</div></div>
</div>
<div style="font-size:56px;font-weight:700;margin-top:70px;color:#23395B">{a}</div>
<div style="font-size:26px;color:#5A6272;margin-top:26px">{b}</div>
<div style="font-size:26px;color:#3E6B48;margin-top:12px;font-weight:700">{c}</div>
</div></body></html>"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":1200,"height":630})
    for l,(a,bb,c,f) in T.items():
        pg.set_content(HTML.format(a=a,b=bb,c=c,f=f)); pg.wait_for_timeout(200)
        pg.screenshot(path=f"{D}/og-{l}.png")
    b.close()
print("ok")
