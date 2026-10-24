import sys
sys.stdout.reconfigure(encoding='utf-8')
import asyncio
from playwright.async_api import async_playwright

async def run_flow():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, channel='chrome')
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        print("Navigating to live application...")
        await page.goto('https://slothchef-ai.onrender.com/', wait_until='networkidle')
        await page.wait_for_timeout(1000)
        
        print("Opening 1-Click Disasters...")
        await page.get_by_text("1-Click Disasters").click()
        await page.wait_for_timeout(800)
        
        print("Selecting Post-Deploy Desperation...")
        await page.get_by_text("Post-Deploy Desperation").click()
        await page.wait_for_timeout(1000)
        await page.screenshot(path='video_production/assets/footage/shot_preset_selected.png')
        
        print("Clicking Synthesize Sloth Meal...")
        await page.get_by_text("Synthesize Sloth Meal").click()
        
        # Wait for recipe to appear (look for Midnight Dan-Dan Rescue or recipe title)
        print("Waiting for generated recipe...")
        await page.wait_for_timeout(3500)
        await page.screenshot(path='video_production/assets/footage/shot_recipe_generated.png')
        
        # Check Cook-Along mode
        cook_along_btn = page.get_by_text("Cook-Along Mode")
        if await cook_along_btn.count() > 0:
            print("Switching to Cook-Along Mode...")
            await cook_along_btn.click()
            await page.wait_for_timeout(1000)
            await page.screenshot(path='video_production/assets/footage/shot_cook_along.png')
            
        # Check TabPFN Math modal
        tabpfn_btn = page.get_by_text("TabPFN Math")
        if await tabpfn_btn.count() > 0:
            print("Opening TabPFN Math modal...")
            await tabpfn_btn.click()
            await page.wait_for_timeout(1000)
            await page.screenshot(path='video_production/assets/footage/shot_tabpfn_modal.png')
            
        print("Flow completed successfully!")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(run_flow())
