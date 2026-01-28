const http = require('http');
const fs = require('fs');
const path = require('path');
const https = require('https');

const PORT = 3000;
const BRAVE_API_KEY = "BSAHVdH4_22L2EwR1duGJpF8wDrh4MJ";

const MIMES = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'text/javascript',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.json': 'application/json'
};

const server = http.createServer((req, res) => {
    console.log(`${req.method} ${req.url}`);

    // --- API: Web Search Proxy ---
    if (req.url.startsWith('/api/search')) {
        const urlParams = new URL(req.url, `http://${req.headers.host}`).searchParams;
        const query = urlParams.get('q');

        if (!query) {
            res.writeHead(400, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Missing query' }));
            return;
        }

        const braveUrl = `https://api.search.brave.com/res/v1/web/search?q=${encodeURIComponent(query)}`;

        const proxyReq = https.request(braveUrl, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'X-Subscription-Token': BRAVE_API_KEY
            }
        }, (proxyRes) => {
            res.writeHead(proxyRes.statusCode, { 'Content-Type': 'application/json' });
            proxyRes.pipe(res);
        });

        proxyReq.on('error', (e) => {
            console.error(e);
            res.writeHead(500, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Search failed' }));
        });

        proxyReq.end();
        return;
    }

    // --- Static File Serving ---
    let filePath = '.' + req.url;
    if (filePath === './') filePath = './index.html';

    const extname = path.extname(filePath);
    const contentType = MIMES[extname] || 'application/octet-stream';

    fs.readFile(filePath, (error, content) => {
        if (error) {
            if (error.code === 'ENOENT') {
                res.writeHead(404);
                res.end('404 Not Found');
            } else {
                res.writeHead(500);
                res.end('500 Internal Server Error: ' + error.code);
            }
        } else {
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(content, 'utf-8');
        }
    });
});

server.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}/`);
    console.log(`- Web Search API enabled at /api/search`);
});
