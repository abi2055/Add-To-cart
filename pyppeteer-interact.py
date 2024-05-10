import asyncio
from pyppeteer import launch, connect

#  Calculate and get the midpoint of the bounding box coordinates
def get_centers(*xyxy):
    x1, y1, x2, y2 = xyxy
    x_center = x1 + (x2 - x1) / 2
    y_center = y1 + (y2 - y1) / 2
    return x_center, y_center


async def main():
    # browser = await launch(
    #    headless=False,
    #    # slowMo=250
    # )
    browser = await connect(
        browserWSEndpoint='ws://127.0.0.1:9222/devtools/browser/60cdc046-1c28-454d-ae5b-5c583215f935',
        # slowMo=100
    )
    
    page = await browser.newPage()

    await page.setViewport(viewport={'width': 1280, 'height': 800})

    # Go to Amazon.com homepage
    await page.goto(
        url='https://www.amazon.com/ref=nav_logo',
        options={
            'waitUntil': 'load',
        }
    )

    # Take a screenshot of the page and save to a base64 string
    # const screenshot = await page.screenshot(encoding='base64')

    # Send the base64 string of the image to the model for detection

    # 1st Product: [317.0,495.0,555.0,574.0]
    # Deliver to link: [149.0,13.0,287.0,51.0]
    # Groceries link: [211.0,68.0,312.0,90.0]
    # Best Sellers link: [313.0,68.0,412.0,90.0]
    # 3rd Product Image: [909,323,1144,492]
    # 3rd Product Link: [909,497,1150,574] 
    # Right Scroll Button: [1215,400,1258,440]
    # Left Scroll Button: [217,401,261,440]


    # Click on the Best Sellers link
    xyxy = [312.0, 68.0, 400.0,90.0] 

    # Move the mouse to the center of the bounded box
    x_center, y_center = get_centers(*xyxy)
    await page.mouse.move(x_center, y_center)
    await page.mouse.click(x_center, y_center)

    await page.waitForNavigation()

    for i in range(4):
        # Locate and click the scroll left button
        xyxy = [217,401,261,440]

        x_center, y_center = get_centers(*xyxy)
        await page.mouse.move(x_center, y_center)
        await page.mouse.click(x_center, y_center)

        await page.waitFor(1300)

    # Then click the 1st product link
    xyxy = [317.0,495.0,555.0,574.0]

    x_center, y_center = get_centers(*xyxy)
    await page.mouse.move(x_center, y_center)
    await page.mouse.click(x_center, y_center)
    
    await page.waitForNavigation()

    for i in range(6):
        await page.keyboard.press(key='ArrowDown')

    # Then locate and click the add to cart button
    x_center, y_center = [1138.5, 633.5] # width: 209, "height": 37,
    await page.mouse.move(x_center, y_center)
    await page.mouse.click(x_center, y_center)

    # wait for navigation complete
    await page.waitForNavigation()

    # Then locate and click the view cart link
    x_center, y_center = [982, 230] # width: 236, height: 38

    await page.mouse.move(x_center, y_center)
    await page.mouse.click(x_center, y_center)

    # Wait for navigation to complete
    await page.waitForNavigation()
    
    # await page.close()
    # await browser.disconnect()
    # await browser.close()

asyncio.get_event_loop().run_until_complete(main())
