function startDetection() {
  fetch('/start', { method: 'POST' })
    .then(response => response.text())
    .then(data => {
      document.getElementById('status').textContent = data;
    });
}

function stopDetection() {
  fetch('/stop')
    .then(response => response.text())
    .then(data => {
      document.getElementById('status').textContent = data;
    });
}
