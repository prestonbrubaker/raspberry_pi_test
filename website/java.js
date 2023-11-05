// This function fetches the data from the data.json file
function fetchData() {
  fetch('data.json')
    .then(response => response.json()) // Parse the JSON from the response
    .then(data => {
      // Update the DOM elements with the data
      document.getElementById('total-loads').textContent = data.total_loads;
      document.getElementById('unique-devices').textContent = data.unique_visitors.length;
    })
    .catch(error => {
      // Handle any errors here
      console.error('Error fetching data:', error);
    });
}

// Call the function when the script loads
fetchData();
