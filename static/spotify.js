"use strict";

function setTimer(){
  console.log( "timer set" );
  setInterval(refresh_Token,360000);
};

function refresh_Token(){
  $.get('/refresh-token', function() {
    console.log('token refresh');
  });
};


$(document).ready(setTimer);
