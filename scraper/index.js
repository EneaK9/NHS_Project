const fs = require('fs');
const { chromium } = require('playwright');

const BASE_URL = "https://www.nhs.uk/conditions/";

(async () => {
    const browser = await chromium.launch({ headless: false });
    const page = await browser.newPage();

    console.log("🔄 Scraping NHS conditions...");
    await page.goto(BASE_URL, { waitUntil: "domcontentloaded" });

    await page.waitForSelector("a", { timeout: 15000 });


    const conditions = await page.evaluate(() => {
        return Array.from(document.querySelectorAll("a.nhsuk-card__link, a.nhsuk-list-panel__link"))
            .map(link => ({
                title: link.innerText.trim(),
                url: link.href.startsWith("http") ? link.href : `https://www.nhs.uk${link.getAttribute("href")}`
            }));
    });

    console.log(`✅ Found ${conditions.length} conditions!`);

    if (conditions.length === 0) {
        console.error("❌ No conditions found. Check if the page structure has changed.");
    } else {
        let detailedArticles = [];

        for (const condition of conditions) {
            console.log(`📖 Scraping: ${condition.title} (${condition.url})`);
            await page.goto(condition.url, { waitUntil: "domcontentloaded" });

            // Extract the main content
            const content = await page.$eval("div.nhsuk-main-wrapper", el => el.innerText.trim());

            detailedArticles.push({ 
                title: condition.title, 
                url: condition.url, 
                content: content 
            });

            // Avoid getting blocked (wait 2 seconds before next request)
            await page.waitForTimeout(2000);
        }

        fs.writeFileSync("nhs_conditions.json", JSON.stringify(detailedArticles, null, 2));
        console.log("✅ Conditions scraped and saved!");
    }

    await browser.close();
})();
