// Toggle slides

$(document).ready(function(){


  $('#toggle').click(function(e) {
    e.preventDefault();
    console.log('from toggle slide function');
    $('.slide-in').toggleClass('show');
});

  $('#toggle-delete').click(function(e) {
    // console.log('from toggle slide function ***');
    e.preventDefault();
    $('.slide-in').toggleClass('show');
});

});
