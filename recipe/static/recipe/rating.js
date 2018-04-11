'use strict'

$(document).ready(function() {
  $('#rating-container button').click(function() {
    let selectedRating = $(this).attr('value');
    updateRating(selectedRating);
  });

  function updateRating(value) {
    let data = JSON.stringify({ 'rating': value });
    let request = new XMLHttpRequest();
    request.open('POST', URL_RATE, true);
    request.setRequestHeader("Content-Type", "application/json; charset=utf-8");
    request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    request.onreadystatechange = function() {
      if(request.readyState == 4 && request.status == 200) {
        parseResponse(request.responseText);
      }
    };
    request.send(data);
  }

  function parseResponse(r) {
    let response = JSON.parse(r);
    if(response.valid) {
      updateRatingDisplay(response.average, response.count);
    }
  };

  function updateRatingDisplay(value, count) {
    $('#rating').html('Rating: ' + value + " (" + count + ")");
  };

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
