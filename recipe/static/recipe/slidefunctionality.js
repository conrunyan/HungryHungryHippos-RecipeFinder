$(document).ready(function() {
  var slideout = new Slideout({
    'panel': document.getElementById('panel'),
    'menu': document.getElementById('menu'),
    'padding': 0,
    'tolerance': 70
  });

  // Toggle button
  $('.toggle-button').on('click', function() {
    slideout.toggle();
  });

});
