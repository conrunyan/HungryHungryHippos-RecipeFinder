'use strict'

$(document).ready(function() {
  let NOT_FAVORITE = "https://d30y9cdsu7xlg0.cloudfront.net/png/773084-200.png";
  let FAVORITE = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Heart_coraz%C3%B3n.svg/1200px-Heart_coraz%C3%B3n.svg.png";
  let favorited = IS_FAVORITE;

  updateColSize();
  updateImage($("#favorite"))

  $("#favorite").click(function() {
    if (favorited === 1) {
      favorited = 0;
      updateImage($(this));
    } else {
      favorited = 1;
      updateImage($(this));
    }
    let value = URL_RATE;
    parseRequest($(this));
  });

  $("#favorite").hover(function() {
    hoverImage($(this));
  }, function() {
    hoverImage($(this));
  });

  function updateImage(div) {
    let src;
    if (favorited) { src = FAVORITE; }
    else { src = NOT_FAVORITE; }
    div.attr("src", src);
  }

  function hoverImage(div) {
    let src = div.attr("src");
    if (src === FAVORITE) {
      div.attr("src", NOT_FAVORITE);
    } else {
      div.attr("src", FAVORITE);
    }
  }

  function parseRequest(div) {
    let body = JSON.stringify({'isFavorite': favorited});
    let request = new XMLHttpRequest();
    request.open('POST', URL_FAV, true);
    request.setRequestHeader("Content-Type", "application/json; charset=utf-8");
    request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    request.onreadystatechange = function() {
      if(request.readyState == 4 && request.status == 200) {
        hoverImage(div);
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

  function updateColSize() {
    let width = $(window).width();
    if (width < 400) {
      $(".ingredients-list").css("-webkit-column-count", "1");
      $(".ingredients-list").css("-moz-column-count", "1");
      $(".ingredients-list").css("column-count", "1");
    }
  }
});
