const http = require("node:http");
const fs = require("node:fs");
const path = require("node:path");
const { spawnSync } = require("node:child_process"); // use spawnSync, not exec or spawn, to block while waiting for python script to finish

const HOSTNAME = "127.0.0.1";
const PORT = 8080;

const _api_post_interest = (req, res) => {

    /* agglomorate the data as they come in */
    let body = '';
    req.on('data', (chunk) => {
        body += chunk.toString();
    });

    /* once the data have all come in, handle it */
    req.on('end', () => {
        try {
            /* expecting json (client js sends json). decode it here */
            const data = JSON.parse(body);
            const interest = data.interestEntry;
            console.log('Received interest: ', interest);
            
            /* if all is successful so far, run the ai with the sent data */
            console.log(`Executing with ${interest}`);
            const aiProc = spawnSync("python3", ["prereq_calc/ai.py", `"${interest}"`]); // wrap interest in quotes so shell takes in spaces in prompt
            
            if (aiProc.error) {
                // if some general error happened... log it and tell the user
                console.error('Error executing Python script: ', aiProc.error);
                res.writeHead(500, { 'Content-Type': 'text/plain' });
                res.end('Internal error!');
            } else if (aiProc.status !== 0) {
                // log stderr for posterity & tell requester that something happened with the script
                console.error('Script exited with non-zero status code: ', aiProc.status);
                res.writeHead(500, { 'Content-Type': 'text/plain' });
                res.end('Internal error!');
            } else {
                // the results from stdout being sent to the requester
                console.log('Output: ', aiProc.stdout.toString());
                res.writeHead(200, { 'Content-Type': 'text/plain' });
                res.end(aiProc.stdout);
            }

            console.log(`Finished executing with ${interest}`);
        } catch (error) {
            console.error('Error parsing JSON:', error);
            res.writeHead(400, { 'Content-Type': 'text/plain' });
            res.end('Invalid JSON');
        }
    });
}

const _webpage = (req, res) => {
    let requestedFile = "." + req.url; // make the request into a searchable path
    if (requestedFile == "./") requestedFile = "./index.html";

    /* figure out what type of file is being requested and set the header accordingly */
    const extension = path.extname(requestedFile);
    let contentType;
    switch(extension){
        case(".html"):
            contentType = "html";
            break;
        case(".css"):
            contentType = "css";
            break;
        case(".js"):
            contentType = "javascript";
            break;
    }
    res.setHeader("Content-Type", `text/${contentType}`);

    fs.readFile(path.join(__dirname, requestedFile), (err, data) => {
        if(err) {
            res.writeHead(500);
            res.end(`Error fetching ${req.url}`);
            return;
        }
        res.writeHead(200);
        res.end(data);
    });
}

const server = http.createServer((req, res) => {
    /* section for api */
    if (req.method === 'POST' && req.url === '/postInterest')
        _api_post_interest(req, res);

    /* webpage functionality */
    else
        _webpage(req, res);
});

server.listen(PORT, HOSTNAME, () => {
    console.log(`Server running at ${HOSTNAME}:${PORT}`);
});