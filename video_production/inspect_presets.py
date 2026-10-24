import sys
sys.stdout.reconfigure(encoding='utf-8')
import asyncio
from playwright.async_api import async_playwright

async def inspect_presets():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, channel='chrome')
        page = await browser.new_page()
        await page.goto('https://slothchef-ai.onrender.com/', wait_until='networkidle')
        
        # Click the 1-Click Disasters button
        btn = page.get_by_text("1-Click Disasters")
        await btn.click()
        await page.wait_for_timeout(1000)
        
        # Take screenshot of the presets popup or drawer
        await page.screenshot(path='video_production/assets/footage/shot_presets_open.png')
        print("Presets screenshot saved.")
        
        # Check text on page
        texts = await page.locator("button, h3, h4, [role='dialog']").all_inner_texts()
        print("Relevant texts:")
        for t in texts:
            if any(k in t for k in ['Ramen', 'Deploy', 'Desperation', 'Post', 'Hangover', 'Midnight']):
                print("Match:", t.strip().replace('\n', ' -- '))
                
        await browser.close()

if __name__ == '__main__':
    asyncio.run(inspect_presets())
