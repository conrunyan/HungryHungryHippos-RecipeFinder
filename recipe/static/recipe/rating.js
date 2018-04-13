'use strict'

$(document).ready(function() {
  let currentUserRating = null;
  let currentAverageRating = null;
  let entered = false;
  refreshRating();

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
      currentUserRating = response.user_rating;
      currentAverageRating = response.average;

      updateRatingDisplay(response.user_rating, response.average, response.count);
    }
  };

  function updateRatingDisplay(user_rating, average, count) {
    let value = average;
    if(user_rating) {
      value = user_rating;
    }
    if(!value) {
      value = 0;
    }

    const TOTAL_STARS = 5;
    let fullStars = Math.floor(value);

    let ratingStars = $("#rating-stars");
    ratingStars.empty();
    for(var i = 1; i <= fullStars; i++) {
      ratingStars.append(createFullStar(i, user_rating));
    }

    for(var i = fullStars + 1; i <= TOTAL_STARS; i++) {
      ratingStars.append(createEmptyStar(i));
    }

    if(count !== null)
      $('#rating-count').html('(' + count + ')');
  };

  function createFullStar(value, shouldBeGold) {
    return createStar(value, shouldBeGold ? IMG_STAR_FULL : IMG_STAR_FULL_GRAY);
  }

  function createEmptyStar(value) {
    return createStar(value, IMG_STAR_EMPTY);
  }

  function createStar(value, url) {
    let img = $("<img/>", {
      id: "star-" + value,
      class: "star",
      alt: "star",
      src: url,
      value: value,
    });

    if(IS_AUTHENTICATED) {
      img.click(function() {
        let selectedRating = $(this).attr('value');
        updateRating(selectedRating);
      });

      img.mouseenter(function() {
        if(entered) {
          return;
        }
        entered = true;
        let selectedRating = $(this).attr('value');
        updateRatingDisplay(selectedRating, 0, null);
      });

      img.mouseleave(function() {
        entered = false;
        updateRatingDisplay(currentUserRating, currentAverageRating, null);
      });
    }

    return img;
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
