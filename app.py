import os
import asyncio
from flask import Flask, request, jsonify
from playwright.async_api import async_playwright

app = Flask(__name__)

async def scrape_nw_link(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        await context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        cookie_val = os.environ.get("NW_COOKIE", "")
        if cookie_val:
            await context.set_extra_http_headers({"Cookie": cookie_val})

        page = await context.new_page()
        await page.goto(url, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        
        content = await page.content()
        await browser.close()
        return content

@app.route('/parse_nw', methods=['POST'])
def parse_nw():
    data = request.get_json()
    link = data.get('url') if data else None
    if not link:
        return jsonify({'error': 'Missing url parameter'}), 400
    try:
        html_content = asyncio.run(scrape_nw_link(link))
        return jsonify({'status': 'success', 'content': html_content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
