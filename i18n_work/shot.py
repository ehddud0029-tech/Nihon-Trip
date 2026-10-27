import sys
from playwright.sync_api import sync_playwright
lang=sys.argv[1]; W=int(sys.argv[2]) if len(sys.argv)>2 else 1300
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":W,"height":900})
    errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.goto(f"file:///home/claude/site/index.html?lang={lang}"); pg.wait_for_timeout(700)
    for v,ev in [("home","1"),("spots","st.city='osaka';st.area='all';render()"),("food","st.city='tokyo';st.area=areasOf('tokyo')[1].key;render()"),("transport","st.city='fukuoka';st.area='all';render()"),("shopping","st.city='hokkaido';st.area='all';render()"),("festivals","st.city='all';render()")]:
        pg.evaluate(f"()=>go(\"{v}\")"); pg.wait_for_timeout(200)
        pg.evaluate(f"()=>{{{ev}}}"); pg.wait_for_timeout(300)
        pg.screenshot(path=f"/tmp/claude-0/shots/{lang}_{W}_{v}.png", full_page=False)
    print(errs)
    b.close()
