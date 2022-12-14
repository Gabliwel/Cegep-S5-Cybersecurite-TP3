const puppeteer = require('puppeteer');

(async () => {

    console.log('start');
    const browser = await puppeteer.launch({
        userDataDirL: "./user_data",
        headless: true,
        args:['--no-sandbox']
    });

    console.log('csrf');
    console.log('loading #1');

    const page = await browser.newPage();
    await page.goto('http://frontEnd:5556/');
    await page.type('#username', 'Boromir');
    await page.type('#password', 'e88250080bb4e646862da1c9aba6e68609e70500');
    await page.click('#login')
    await page.waitForNavigation();
    await page.waitForTimeout(2000);

    console.log('loading #2');
    const page2 = await browser.newPage();
    await page2.goto('http://csrf:5557/');

    //bodyHTML = await page2.evaluate(() =>  document.documentElement.outerHTML);
    //console.log(bodyHTML)

    await page2.waitForNavigation();
    
    console.log('xss');

    const page3 = await browser.newPage();
    await page3.goto('http://frontEnd:5556/');
    await page3.type('#username', 'Gandalf');
    await page3.type('#password', 'e88250080bb4e646862da1c9aba6e68609e70500');
    await page3.click('#login')
    await page3.waitForNavigation();
    await page3.waitForTimeout(2000);

    while(true)
    {
        await page3.click('#viewFaq')
        await page3.waitForTimeout(30000);
    }

    console.log('closing....');
    await browser.close();

}) ();