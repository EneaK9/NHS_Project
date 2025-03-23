const express = require("express");
const cors = require("cors"); // Import CORS
const fs = require('fs');
const path = require('path');

const app = express();
app.use(cors()); // Enable CORS

app.get('/api/data', (req, res) => {
    // Path to your JSON files directory
    const directoryPath = path.resolve(__dirname, 'translated_nhs');

    // Read all JSON files in the directory
    fs.readdir(directoryPath, (err, files) => {
        if (err) {
            return res.status(500).json({ message: 'Error reading directory' });
        }

        // Filter out non-JSON files
        const jsonFiles = files.filter(file => file.endsWith('.json'));

        // Read and parse each JSON file
        const dataPromises = jsonFiles.map(file => {
            return new Promise((resolve, reject) => {
                fs.readFile(path.join(directoryPath, file), 'utf-8', (err, data) => {
                    if (err) {
                        reject(err);
                    } else {
                        const jsonData = JSON.parse(data);
                        const responseData = {
                            title: jsonData.title,
                            sections: jsonData.sections.map((section) => ({
                                title: section.title,
                                paragraphs: section.paragraphs
                            })),
                            sublinks: jsonData.sublinks || [] // Include the top-level sublinks if they exist
                        };
                        resolve(responseData);
                    }
                });
            });
        });

        // Send the response once all files are read and parsed
        Promise.all(dataPromises)
            .then(dataArray => {
                res.json(dataArray);
            })
            .catch(error => {
                res.status(500).json({ message: 'Error reading JSON files', error });
            });
    });
});

// New route to handle requests for individual articles
app.get('/api/data/:articleName', (req, res) => {
    const articleName = req.params.articleName;
    const directoryPath = path.resolve(__dirname, 'translated_nhs');
    const filePath = path.join(directoryPath, `${articleName}.json`);

    fs.readFile(filePath, 'utf-8', (err, data) => {
        if (err) {
            return res.status(404).json({ message: 'Article not found' });
        }

        try {
            const jsonData = JSON.parse(data);
            const responseData = {
                title: jsonData.title,
                sections: jsonData.sections.map((section) => ({
                    title: section.title,
                    paragraphs: section.paragraphs
                })),
                sublinks: jsonData.sublinks || [] // Include the top-level sublinks if they exist
            };
            res.json(responseData);
        } catch (error) {
            res.status(500).json({ message: 'Error parsing JSON', error });
        }
    });
});

// New route to handle search requests
app.get('/api/search', (req, res) => {
    const query = req.query.q.toLowerCase();
    const directoryPath = path.resolve(__dirname, 'translated_nhs');

    fs.readdir(directoryPath, (err, files) => {
        if (err) {
            return res.status(500).json({ message: 'Error reading directory' });
        }

        const jsonFiles = files.filter(file => file.endsWith('.json'));

        const searchPromises = jsonFiles.map(file => {
            return new Promise((resolve, reject) => {
                fs.readFile(path.join(directoryPath, file), 'utf-8', (err, data) => {
                    if (err) {
                        reject(err);
                    } else {
                        const jsonData = JSON.parse(data);
                        const titleMatch = jsonData.title.toLowerCase().includes(query);
                        const contentMatch = jsonData.sections.some(section =>
                            section.title.toLowerCase().includes(query) ||
                            section.paragraphs.some(paragraph => paragraph.toLowerCase().includes(query))
                        );

                        if (titleMatch || contentMatch) {
                            resolve({
                                title: jsonData.title,
                                sections: jsonData.sections.map((section) => ({
                                    title: section.title,
                                    paragraphs: section.paragraphs
                                })),
                                sublinks: jsonData.sublinks || []
                            });
                        } else {
                            resolve(null);
                        }
                    }
                });
            });
        });

        Promise.all(searchPromises)
            .then(results => {
                const filteredResults = results.filter(result => result !== null);
                res.json(filteredResults);
            })
            .catch(error => {
                res.status(500).json({ message: 'Error searching articles', error });
            });
    });
});

app.listen(5000, () => {
    console.log("Server running on port 5000");
});