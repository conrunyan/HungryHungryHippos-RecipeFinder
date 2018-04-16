'use strict'

$(document).ready(function() {
  // let COLLAPSED_SRC = "http://icons.iconarchive.com/icons/awicons/vista-artistic/128/add-icon.png";
  // let EXPANDED_SRC = "https://cdn1.iconfinder.com/data/icons/basic-ui-elements-color/700/07_minus-128.png";
  let COLLAPSED_SRC = "https://cdn2.iconfinder.com/data/icons/ios-7-icons/50/down4-512.png";
  let EXPANDED_SRC = "https://cdn2.iconfinder.com/data/icons/ios-7-icons/50/up4-256.png";

  var listOfIngredients = [];
  var listOfAppliances = [];
  var listOfDifficulties = [];
  var listOfTimes = [];
  var allFilters = [];
  var panelIsOpen = false;

  updateImage($(".update-on-expand"), COLLAPSED_SRC);
  checkPersistentIngredients(PERSISTENT_INGREDIENTS);
  queryRecipes();

  $(".update-on-expand").on('show.bs.collapse', function() {
    updateImage($(this), EXPANDED_SRC);
  });

  $(".update-on-expand").on('hide.bs.collapse', function() {
    updateImage($(this), COLLAPSED_SRC);
  });

  $(".update-list").change(function() {
    addToList($(this), listOfIngredients);
  });

  $(".update-appliance").change(function() {
    addToList($(this), listOfAppliances);
  });

  $(".update-difficulty").change(function() {
    addToList($(this), listOfDifficulties);
  });

  $(".update-time").change(function() {
    addToList($(this), listOfTimes);
  });

  $("#run-search").click(function() {
    if (!panelIsOpen) {
      panelIsOpen = true;
    } else {
      panelIsOpen = false;
      queryRecipes();
    }
  });

  $("#menu").click(function(){
    if (event.target.id != "myInput") {
      $(".dropdown-content").hide();
    }
  });

  $(".filterFunction").click(function() {
    setSizeOfSlideout();
    $(".dropdown-content").show();
  });

  $(".filterFunction").keyup(function() {
    var input = $("#myInput");
    var filter = input.val().toUpperCase();
    var div = $("#searchDropdown");
    var a = div.find("a");
    for (var i = 0; i < a.length; i++) {
        if (a[i].innerHTML.toUpperCase().indexOf(filter) > -1) {
            a[i].style.display = "";
        } else {
            a[i].style.display = "none";
        }
    }
  });

  $(".searched-ingredient").click(function() {
    var ing = $(this).text();
    var val = $('input[value="'+ing+'"]');
    val.prop('checked', true);
    addToList(val, listOfIngredients);
    $(".dropdown-content").hide();
  });

  $("#clear-ingredients").click(function() {
    for (let i in listOfIngredients) {
      let ing = $('input[type=checkbox][value="'+listOfIngredients[i]+'"]');
      ing.prop('checked', false);
    }
    for (let i in listOfAppliances) {
      let app = $('input[type=checkbox][value="'+listOfAppliances[i]+'"]');
      app.prop('checked', false);
    }
    for (let i in listOfDifficulties) {
      let diff = $('input[type=checkbox][value="'+listOfDifficulties[i]+'"]');
      diff.prop('checked', false);
    }
    for (let i in listOfTimes) {
      let t = $('input[type=checkbox][value="'+listOfTimes[i]+'"]');
      t.prop('checked', false);
    }
    listOfIngredients = [];
    listOfAppliances = [];
    listOfDifficulties = [];
    listOfTimes = [];
    allFilters = [];
    $("#noIngredients").show();
    deleteRecipesFromPage(listOfIngredients.length);
  });

  function parseResponse(r) {
    let response = JSON.parse(r);
    deleteRecipesFromPage(allFilters.length);
    deleteNext10Button();
    addRecipesToPage(response['results'], 0, 10, allFilters.length);
    runNext10(response['results']);
  }

  function updateImage(div, src) {
    div.siblings().find(".update-image").attr("src", src);
  };

  function addToList(element, list) {
    if (element.prop("checked")) {
      list.push(element.prop("value"));
      allFilters.push(element.prop("value"));
      document.getElementById("noIngredients").style.display = 'none';
    } else {
      let index = list.indexOf(element.prop("value"));
      if (index !== -1) list.splice(index, 1);
      let index2 = allFilters.indexOf(element.prop("value"));
      if (index2 !== -1) allFilters.splice(index, 1);
      if (list.length == 0) {
        document.getElementById("noIngredients").style.display = 'block';
      }
    }
  }

  function getListOfIngredients() {
    return listOfIngredients;
  }


  function setSizeOfSlideout() {
    var size = $('#myInput').width();
    $('#searchDropdown').width(size);
  }

  function checkPersistentIngredients(ingredients) {
    for(var i = 0; i < ingredients.length; i++) {
      var ingredient = ingredients[i];
      var e = $("input[type='checkbox'][value='" + ingredient + "']");
      if(e) {
        e.prop('checked', true);
        addToList(e, listOfIngredients);
      }
    }
  };

  function queryRecipes() {
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
  };

});
