var working = false;
$('.login').on('submit', function(e) {
  e.preventDefault();
  if (working) return;
  working = true;
  var $this = $(this),
    $state = $this.find('button > .state');
  $this.addClass('loading');
  $state.html('Authenticating');
  setTimeout(function() {
    $this.addClass('ok');
    $state.html('Welcome back!');
    setTimeout(function() {
      $state.html('Log in');
      $this.removeClass('ok loading');
      working = false;
    }, 4000);
  }, 3000);
});

document.addEventListener('DOMContentLoaded', function() {
  const showRequirementsButton = document.getElementById('show-requirements-button');
  const requirementsBox = document.getElementById('requirements-box');

  showRequirementsButton.addEventListener('click', function() {
    // Muestra el cuadro de requerimientos al hacer clic en el botón
    requirementsBox.style.display = 'block';
  });
});
