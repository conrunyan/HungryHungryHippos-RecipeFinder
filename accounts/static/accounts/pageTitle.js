'use strict'

$(document).ready(function() {
  let width = $(window).width();
  // console.log(width);
  if (width < 400) {
    $(".page-title").text("HHH");
    $(".page-title").removeClass("mr-auto");
  }
});
