document.addEventListener('DOMContentLoaded', function() {
    const settingsButton = document.getElementById('inner_settings');
    const settingsOptions = document.getElementById('settings_options');
  
    settingsButton.addEventListener('click', function() {
      if (settingsOptions.style.display === 'none' || settingsOptions.style.display === '') {
        settingsOptions.style.display = 'block';
      } else {
        settingsOptions.style.display = 'none';
      }
    });
  
    const buttons = document.querySelectorAll('.siteSelect');
    buttons.forEach(button => {
      button.addEventListener('click', function() {
        this.classList.toggle('selected');
      });
    });
  
    const startButton = document.getElementById('start_scrape');
    startButton.addEventListener('click', function() {
      const selectedSites = [];
      buttons.forEach(button => {
        if (button.classList.contains('selected')) {
          selectedSites.push(button.id);
        }
      });
      console.log('Selected sites:', selectedSites);
      // Send the selectedSites array to the backend
      fetch('http://localhost:5000/start_scrape', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ selectedSites }),
      })
      .then(response => response.json())
      .then(data => {
        console.log('Success:', data);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
    });
  });