"use strict";

$(function() {    
    $("#search-input").on('input', function(e) {
        if($("#search-input").val().length) {
            $("#search-input-cancel").show();
        }
        else {
            $("#search-input-cancel").hide();
        }
    });
    $("#search-input-cancel").click(function(e) {
        if($("#search-input").val().length) {
            $("#search-input").val("");
            $("#search-input-cancel").hide();
        }
    });
    
});