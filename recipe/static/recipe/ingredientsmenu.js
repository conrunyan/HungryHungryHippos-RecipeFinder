'use strict'

$(document).ready(function() {
  // let COLLAPSED_SRC = "http://icons.iconarchive.com/icons/awicons/vista-artistic/128/add-icon.png";
  // let EXPANDED_SRC = "https://cdn1.iconfinder.com/data/icons/basic-ui-elements-color/700/07_minus-128.png";
  let COLLAPSED_SRC = "https://cdn2.iconfinder.com/data/icons/ios-7-icons/50/down4-512.png";
  let EXPANDED_SRC = "https://cdn2.iconfinder.com/data/icons/ios-7-icons/50/up4-256.png";

  var listOfIngredients = [];
  var panelIsOpen = false;

  updateImage($(".update-on-expand"), COLLAPSED_SRC);
  checkPersistentIngredients(PERSISTENT_INGREDIENTS);

  $(".update-on-expand").on('show.bs.collapse', function() {
    updateImage($(this), EXPANDED_SRC);
  });

  $(".update-on-expand").on('hide.bs.collapse', function() {
    updateImage($(this), COLLAPSED_SRC);
  });

  $(".update-list").change(function() {
    addToList($(this));
  });

  $("#run-search").click(function() {
    if (!panelIsOpen) {
      panelIsOpen = true;
    } else {
      panelIsOpen = false;
      var request = new XMLHttpRequest();
      var params = JSON.stringify(listOfIngredients);
      request.open('POST', URL_ALG_REQUEST, true);
      request.setRequestHeader("Content-Type", "application/json; charset=utf-8");
      request.onreadystatechange = function() {
        if(request.readyState == 4 && request.status == 200) {
          parseResponse(request.responseText);
        }
      };
      request.send(params);
    }
  });

  function parseResponse(r) {
    let response = JSON.parse(r);
    console.log(response);
  }

  function updateImage(div, src) {
    div.siblings().find(".update-image").attr("src", src);
  };

  function addToList(element) {
    if (element.prop("checked")) {
      listOfIngredients.push(element.prop("value"));
      document.getElementById("noIngredients").style.display = 'none';
    } else {
      var index = listOfIngredients.indexOf(element.prop("value"));
      if (index !== -1) listOfIngredients.splice(index, 1);
      if (listOfIngredients.length == 0) {
        document.getElementById("noIngredients").style.display = 'block';
      }
    }
  }

  function getListOfIngredients() {
    return listOfIngredients;
  }

  function checkPersistentIngredients(ingredients) {
    for(var i = 0; i < ingredients.length; i++) {
      var ingredient = ingredients[i];
      var e = $("input[type='checkbox'][value='" + ingredient + "']");
      if(e) {
        e.prop('checked', true);
        addToList(e);
      }
    }
  };
});
