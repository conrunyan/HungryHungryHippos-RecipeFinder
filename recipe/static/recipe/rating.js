'use strict'

$(document).ready(function() {
  refreshRating();


  $('#rating-container button').click(function() {
    let selectedRating = $(this).attr('value');
    updateRating(selectedRating);
  });

  // need to do it this way since stars are added dynamically
  $(document).on('click', '.star', function() {
    let selectedRating = $(this).attr('value');
    updateRating(selectedRating);
  });

  // ditto to hover
  $(document).on('hover', '.star', function() {

  });

  function refreshRating() {
    let request = new XMLHttpRequest();
    request.open('GET', URL_RATE, true);
    request.setRequestHeader("Content-Type", "application/json; charset=utf-8");
    request.onreadystatechange = function() {
      if(request.readyState == 4 && request.status == 200) {
        parseResponse(request.responseText);
      }
    };
    request.send();
  }

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
      updateRatingDisplay(response.user_rating, response.average, response.count);
    }
  };

  function updateRatingDisplay(user_rating, average, count) {
    let value = average;
    if(user_rating) {
      value = user_rating;
    }

    const TOTAL_STARS = 5;
    let fullStars = Math.floor(value);

    let html = "";
    for(var i = 1; i <= fullStars; i++) {
      html += createFullStar(i, user_rating);
    }

    for(var i = fullStars + 1; i <= TOTAL_STARS; i++) {
      html += createEmptyStar(i);
    }

    $('#rating-stars').html(html);
    $('#rating-count').html('(' + count + ')');
  };

  function createFullStar(value, shouldBeGold) {
    return createStar(value, shouldBeGold ? IMG_STAR_FULL : IMG_STAR_FULL_GRAY);
  }

  function createEmptyStar(value) {
    return createStar(value, IMG_STAR_EMPTY);
  }

  function createStar(value, url) {
    let html = '<img id="star-' + value + '" class="star" alt="star" src="' + url + '" ';
    html += 'value="' + value + '" />';
    return html;
  }

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
