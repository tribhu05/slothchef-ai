import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import asyncio
from playwright.async_api import async_playwright

RECORDING_DIR = os.path.abspath("video_production/assets/footage/raw_recordings")
os.makedirs(RECORDING_DIR, exist_ok=True)

async def record_demo():
    print("Starting Playwright video recording session...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, channel='chrome')
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            record_video_dir=RECORDING_DIR,
            record_video_size={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()
        
        # 1. Load homepage
        print("1. Loading live site...")
        await page.goto('https://slothchef-ai.onrender.com/', wait_until='networkidle')
        await page.wait_for_timeout(2500)
        
        # 2. Open 1-Click Disasters
        print("2. Opening 1-Click Disasters...")
        disasters_btn = page.get_by_text("1-Click Disasters")
        await disasters_btn.hover()
        await page.wait_for_timeout(800)
        await disasters_btn.click()
        await page.wait_for_timeout(1500)
        
        # 3. Select Post-Deploy Desperation
        print("3. Selecting Post-Deploy Desperation...")
        preset = page.get_by_text("Post-Deploy Desperation")
        await preset.hover()
        await page.wait_for_timeout(1000)
        await preset.click()
        await page.wait_for_timeout(2000)
        
        # 4. Synthesize Sloth Meal
        print("4. Clicking Synthesize Sloth Meal...")
        synth_btn = page.get_by_text("Synthesize Sloth Meal")
        await synth_btn.hover()
        await page.wait_for_timeout(800)
        await synth_btn.click()
        
        # 5. Recipe generated display
        print("5. Viewing generated recipe...")
        await page.wait_for_timeout(4000)
        
        # Scroll smoothly through the recipe details
        print("6. Scrolling through recipe details...")
        await page.mouse.wheel(0, 400)
        await page.wait_for_timeout(2500)
        await page.mouse.wheel(0, 400)
        await page.wait_for_timeout(2500)
        await page.mouse.wheel(0, -800)
        await page.wait_for_timeout(1500)
        
        # 7. Cook-Along Mode
        print("7. Testing Cook-Along Mode...")
        cook_along_btn = page.get_by_text("Cook-Along Mode")
        if await cook_along_btn.count() > 0:
            await cook_along_btn.hover()
            await page.wait_for_timeout(600)
            await cook_along_btn.click()
            await page.wait_for_timeout(3000)
            
            # Step forward
            step2 = page.get_by_text("2", exact=True)
            if await step2.count() > 0:
                await step2.click()
                await page.wait_for_timeout(2000)
            
            # Switch back to overview
            overview_btn = page.get_by_text("Recipe Overview")
            if await overview_btn.count() > 0:
                await overview_btn.click()
                await page.wait_for_timeout(1500)
        
        # 8. Open TabPFN Math Modal
        print("8. Opening TabPFN Math modal...")
        tabpfn_btn = page.get_by_text("TabPFN Math")
        if await tabpfn_btn.count() > 0:
            await tabpfn_btn.hover()
            await page.wait_for_timeout(600)
            await tabpfn_btn.click()
            await page.wait_for_timeout(4000)
        
        print("Closing context to finalize video file...")
        await page.close()
        await context.close()
        await browser.close()
        print("Playwright recording completed!")

if __name__ == '__main__':
    asyncio.run(record_demo())
