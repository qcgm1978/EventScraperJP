const { ipcRenderer } = require("electron");
let pythonProcess;
let siteBack = false;

ipcRenderer.on("childoutput", (event, data) => {
  console.log(data);
  if (document.getElementById("output-box"))
    document.getElementById("output-box").innerText += data;
});

  const settingsButton = document.getElementById('inner_settings');
  const settingsOptions = document.getElementById('settings_options');

  if (settingsButton)  {
    settingsButton.addEventListener('click', function() {
      if (settingsOptions.style.display === 'block' || settingsOptions.style.display === '') {
        settingsOptions.style.display = 'none';
      } else {
        settingsOptions.style.display = 'block';
      }
    });
  }
  const buttons = document.querySelectorAll('.siteSelect');
  buttons.forEach(button => {
    button.addEventListener('click', function() {
      this.classList.toggle('selected');
    });
  });

  const buttons_eplus = document.querySelectorAll('.monthSelect');
  buttons_eplus.forEach(buttons_eplus => {
    buttons_eplus.addEventListener('click', function() {
      this.classList.toggle('selected_eplus');
    });
  });

  const startButton = document.getElementById('start_scrape');
  if (startButton) {
  startButton.addEventListener('click', function() {
    siteBack = false;
    const selectedSites = [];
    buttons.forEach(button => {
      if (button.classList.contains('selected')) {
        selectedSites.push(button.id);
      }
    });
    console.log('Selected sites:', selectedSites);
    if (selectedSites.length === 0) {
      alert('Please select at least one site.');
      return;
    }
    const selectedMonths = [];
    buttons_eplus.forEach(buttons_eplus => {
      if (buttons_eplus.classList.contains('selected_eplus')) {
        selectedMonths.push(buttons_eplus.id);
      }
    });
    console.log('Selected months:', selectedMonths);

    if (selectedMonths.length === 0 && selectedSites.includes('eplus')) {
      alert('Please select at least one month.');
      return;}

    let l_tike_start_date = document.getElementById('l-tike_start_date').value;
    let l_tike_end_date = document.getElementById('l-tike_end_date').value;

    console.log('Selected start date:', l_tike_start_date);
    console.log('Selected end date:', l_tike_end_date);
    
    localStorage.setItem('selectedSites', JSON.stringify(selectedSites));
    localStorage.setItem('selectedMonths', JSON.stringify(selectedMonths));
    localStorage.setItem('l-tike_start_date', JSON.stringify(l_tike_start_date));
    localStorage.setItem('l-tike_end_date', JSON.stringify(l_tike_end_date));

    window.location.href = 'site_scraping.html';
  });}

  if (window.location.pathname.endsWith('site_scraping.html')) {
    const chosenSitesDiv = document.getElementById('chosen-sites');
    const loadingWheelDiv = document.getElementById('loading-wheel');
    const outputBoxDiv = document.getElementById('output-box');
    const exitButton = document.getElementById('exit-button');

    const selectedSites = JSON.parse(localStorage.getItem('selectedSites')) || [];
    const selectedMonths = JSON.parse(localStorage.getItem('selectedMonths')) || [];
    const l_tike_start_date = JSON.parse(localStorage.getItem('l-tike_start_date')) || [];
    const l_tike_end_date = JSON.parse(localStorage.getItem('l-tike_end_date')) || [];

    selectedSites.forEach(site => {
      const img = document.createElement('img');
      img.src = `./${site}.png`;
      img.alt = `${site} logo`;
      img.style.transform = 'scale(0.7)';
      chosenSitesDiv.appendChild(img);
    });

    const loadingWheel = document.createElement('div');
    loadingWheel.className = 'spinner';
    loadingWheelDiv.appendChild(loadingWheel);

    request = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({selectedSites, selectedMonths, l_tike_start_date, l_tike_end_date}),
    };
    console.log('Request:', request);
    fetch('http://localhost:5000/start_scrape', request)
    .then(response => {
      console.log('Raw response:', response);
      return response.json();
    })
    .then(data => {
      console.log('Success:', data);
      loadingWheelDiv.style.display = 'none';
      exitButton.style.display = 'block';
    })
    .catch((error) => {
      console.error('Error:', error);
      loadingWheelDiv.style.display = 'none';
      exitButton.style.display = 'block';
    });

    
    exitButton.addEventListener('click', function() {
      window.close();
    });
  };
  const exitButton = document.getElementById('exit-button');
  if (exitButton)
  exitButton.addEventListener('click', function() {
    window.close();
  });

  const backButton = document.getElementById('back-button');
  if (backButton)
  backButton.addEventListener('click', function() {
    siteBack = true;
  });

