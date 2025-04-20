// geoinit.js
const http = require('http');
const fs = require('fs');

const html = `
<!DOCTYPE html><html><body>
<script>
navigator.geolocation.getCurrentPosition(pos => {
    fetch('/location', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(pos.coords)
    });
});
</script>Fetching location...
</body></html>`;

http.createServer((req, res) => {
    if (req.method === 'GET') {
        res.writeHead(200, {'Content-Type': 'text/html'});
        res.end(html);
    } else if (req.method === 'POST' && req.url === '/location') {
        let data = '';
        req.on('data', chunk => data += chunk);
        req.on('end', () => {
            console.log("📍 Location received:", JSON.parse(data));
            res.end('OK');
            process.exit();
        });
    }
}).listen(3000, () => console.log("Server running at http://localhost:3000"));
