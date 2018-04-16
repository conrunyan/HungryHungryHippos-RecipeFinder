'use strict'

$(document).ready(function() {
  let NOT_FAVORITE = "https://d30y9cdsu7xlg0.cloudfront.net/png/773084-200.png";
  let FAVORITE = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Heart_coraz%C3%B3n.svg/1200px-Heart_coraz%C3%B3n.svg.png";
  let favorited = false;

  updateImage($("#favorite"), NOT_FAVORITE)

  $("#favorite").click(function() {
    if (favorited) {
      updateImage($(this), NOT_FAVORITE);
      favorited = false;
    } else {
      updateImage($(this), FAVORITE);
      favorited = true;
    }
    let value = URL_RATE;
    parseRequest();
  });

  function updateImage(div, src) {
    div.attr("src", src);
  }

  function parseRequest() {
    let body = JSON.stringify({'isFavorite': favorited});
    let request = new XMLHttpRequest();
    request.open('POST', URL_FAV, true);
    request.setRequestHeader("Content-Type", "application/json; charset=utf-8");
    request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    request.onreadystatechange = function() {
      if(request.readyState == 4 && request.status == 200) {
        // parseResponse(request.responseText);
      }
    };
    request.send(body);
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
