import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import Groq from 'groq-sdk';

const app = express();
app.use(cors());
app.use(express.json());

const groq = new Groq({
    apiKey: process.env.GROQ_API_KEY
});

async function translateText(text) {
    try {
        const response = await groq.chat.completions.create({
            model: "llama3-70b-8192", // Groq LLaMA 3 model
            messages: [
                { role: "system", content: "You are a translation assistant. Only return the translated text in Albanian and nothing else. Do not add explanations." },
                { role: "user", content: `Translate this into Albanian: "${text}"` }
            ]
        });

        return response.choices[0].message.content.trim();
    } catch (error) {
        console.error("❌ Translation failed:", error.response ? error.response.data : error.message);
        return text;  // Fallback to original text if translation fails
    }
}

app.post('/translate', async (req, res) => {
    const { text } = req.body;
    if (!text) return res.status(400).json({ error: "Missing text" });

    const translated = await translateText(text);
    res.json({ translated });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`✅ Translation API running on port ${PORT}`);
});