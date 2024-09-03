const CACHE_NAME = "text-to-speech-cache-v2";
const urlsToCache = [
  "/",
  "/static/css/bootstrap.min.css",
  "/static/css/style.css",
  "/static/js/script.js",
  "/static/images/icons/icon-192x192.png",
  "/static/images/icons/icon-512x512.png",
  "/static/images/icons/favicons/favicon.ico",
];

self.addEventListener("install", function (event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function (cache) {
      return cache.addAll(urlsToCache);
    })
  );
});

self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
