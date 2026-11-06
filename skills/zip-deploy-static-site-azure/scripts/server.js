// Minimal dependency-free static file server for an Azure App Service Node stack.
// Azure sets PORT; the Linux Node image runs `npm start`.
const http = require("http"), fs = require("fs"), path = require("path");
const root = __dirname, port = process.env.PORT || 8080;
const types = { ".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript", ".mjs": "text/javascript", ".csv": "text/csv", ".json": "application/json", ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif", ".webp": "image/webp", ".ico": "image/x-icon", ".pdf": "application/pdf", ".md": "text/markdown; charset=utf-8", ".woff2": "font/woff2" };
http.createServer((req, res) => {
  let p = path.normalize(decodeURIComponent(new URL(req.url, "http://x").pathname)).replace(/^(\.\.[\/\\])+/, "");
  if (p.endsWith(path.sep)) p += "index.html";
  const f = path.join(root, p);
  if (!f.startsWith(root)) { res.writeHead(403); return res.end("Forbidden"); }
  fs.readFile(f, (err, buf) => {
    if (err) { res.writeHead(404, { "Content-Type": "text/plain" }); return res.end("Not found"); }
    res.writeHead(200, { "Content-Type": types[path.extname(f).toLowerCase()] || "application/octet-stream" });
    res.end(buf);
  });
}).listen(port, () => console.log("Static site listening on " + port));
