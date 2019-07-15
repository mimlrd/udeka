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


//*--------------- NAVBAR -------------------------------------

// Check for click events on the navbar burger icon
  $(".navbar-burger").click(function() {
      // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
      $(".navbar-burger").toggleClass("is-active");
      $(".navbar-menu").toggleClass("is-active");

  });

  //*--------------- NAVBAR -------------------------------------

});
