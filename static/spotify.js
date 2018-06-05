"use strict";
var timer

function setTimer(){
  timer = setInterval(3600);
}

function refresh_Token(){
  $.get('/refresh-token', setTimer);
}

$("#")
