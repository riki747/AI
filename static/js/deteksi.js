function startDetection() {
  fetch('/start', {
    method: 'POST'
  })
    .then(response => response.text())
    .then(data => {
      document.getElementById('status').textContent = data;
    })
    .catch(error => {
      console.error('Error saat memulai deteksi:', error);
    });
}

function stopDetection() {
  fetch('/stop')
    .then(response => response.text())
    .then(data => {
      document.getElementById('status').textContent = data;
    })
    .catch(error => {
      console.error('Error saat menghentikan deteksi:', error);
    });
}
