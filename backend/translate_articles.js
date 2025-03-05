import 'dotenv/config';
import fs from 'fs';
import axios from 'axios';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const articles = JSON.parse(fs.readFileSync(join(__dirname, '../scraper/nhs_articles.json'), 'utf8')).slice(0, 5); // Limit to 5 articles
const TRANSLATION_API = "http://localhost:5000/translate";

async function translateArticles() {
    let translatedArticles = [];

    for (let i = 0; i < articles.length; i++) {
        console.log(`🔄 Translating article ${i + 1}/${articles.length}: ${articles[i].title}`);

        try {
            const response = await axios.post(TRANSLATION_API, { text: articles[i].title });
            translatedArticles.push({ ...articles[i], translatedTitle: response.data.translated });
            console.log(`✅ Translated: ${articles[i].title} ➝ ${response.data.translated}`);
        } catch (error) {
            console.error(`❌ Error translating ${articles[i].title}:`, error.message);
            translatedArticles.push({ ...articles[i], translatedTitle: articles[i].title });
        }
    }

    fs.writeFileSync('translated_articles.json', JSON.stringify(translatedArticles, null, 2));
    console.log("✅ 5 test articles translated and saved!");
}

translateArticles();
