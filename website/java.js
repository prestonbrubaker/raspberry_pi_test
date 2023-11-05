// This function fetches the data from the data.json file
function fetchData() {
  fetch('data.json')
    .then(response => response.json()) // Parse the JSON from the response
    .then(data => {
      // Log the data or update the DOM elements
      console.log('Total page loads:', data.total_loads);
      console.log('Number of unique devices:', data.unique_ips.length);

      // If you have elements in your HTML to display these values, you can update them like this:
      // document.getElementById('total-loads').textContent = data.total_loads;
      // document.getElementById('unique-devices').textContent = data.unique_ips.length;
    })
    .catch(error => {
      // Handle any errors here
      console.error('Error fetching data:', error);
    });
}

// Call the function when the script loads
fetchData();

