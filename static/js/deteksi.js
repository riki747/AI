function startDetection() {
  fetch('/start', { method: 'POST' })
    .then(response => response.text())
    .then(data => {
      document.getElementById("status").innerText = data;
    })
    .catch(error => {
      document.getElementById("status").innerText = "Gagal memulai: " + error;
    });
}

function stopDetection() {
  fetch('/stop', { method: 'POST' })
    .then(response => response.text())
    .then(data => {
      document.getElementById("status").innerText = data;
    })
    .catch(error => {
      document.getElementById("status").innerText = "Gagal stop: " + error;
    });
}
