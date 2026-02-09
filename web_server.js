const Http = require('http');

const HOST_NAME = '127.0.0.1';
const LISTEN_PORT = 3000;

function handleRequest(request, response) {
    const r = request;
    const res = response;

    let d = '';

    r.on('data', chunk => {
        d += chunk;
    });

    r.on('end', () => {
        res.writeHead(200, {'Content-Type': 'text/plain'});
        if (r.url === '/') {
            res.end("Hello World!");
        } else if (r.url === '/about') {
            res.end("This is an example server.");
        } else {
            res.end("404 Not Found");
        }
    });
}

const SERVER = Http.createServer(handleRequest);

function start_server() {
    SERVER.listen(LISTEN_PORT, HOST_NAME, () => {
        console.log(`Server running at http://${HOST_NAME}:${LISTEN_PORT}/`);
    });
}

start_server();