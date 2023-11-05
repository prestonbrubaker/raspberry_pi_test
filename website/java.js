function fetchData() {
  fetch('data.json?' + new Date().getTime())  // Cache-busting query string
    .then(response => response.json())
    .then(data => {
      document.getElementById('total-loads').textContent = data.total_loads;
      document.getElementById('unique-devices').textContent = data.unique_visitors.length;
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    });
}

fetchData();

