// src/static/js/pending.js
function filterPending() {
    const search = document.getElementById('search').value.toLowerCase();
    fetch(`/pending?search=${encodeURIComponent(search)}`)
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            document.getElementById('pendingTable').innerHTML = doc.getElementById('pendingTable').innerHTML;
        })
        .catch(error => console.error('Error filtering pending:', error));
}