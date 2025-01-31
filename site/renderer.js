const buttons = document.querySelectorAll('.siteSelect');
buttons.forEach(button => {
  button.addEventListener('click', function() {
    this.classList.toggle('selected');
  });
});