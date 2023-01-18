$(document).ready(function(){
    var speed = 300;

    // check for hash and if div exist... scroll to div
    var hash = window.location.hash;
    if($(hash).length) scrollToID(hash, speed);

    // scroll to div on nav click
    $('.scroll-link').click(function (e) {
        e.preventDefault();
        var id = $(this).attr('href');
        if($(id ).length) scrollToID(id, speed);
    });
})

function scrollToID(id, speed) {
    var offSet = 70;
    var obj = $(id).offset();
    var targetOffset = obj.top - offSet;
    $('html,body').animate({ scrollTop: targetOffset }, speed);
}

//New nav
jQuery(function($) {
    $(window).on('scroll', function() {
		if ($(this).scrollTop() >= 200) {
			$('.navbar').addClass('fixed-top');
		} else if ($(this).scrollTop() === 0) {
			$('.navbar').removeClass('fixed-top');

		}
	});

	function adjustNav() {
		var winWidth = $(window).width(),
			dropdown = $('.dropdown'),
			dropdownMenu = $('.dropdown-menu');

		if (winWidth >= 768) {
			dropdown.on('mouseenter', function() {
				$(this).addClass('show')
					.children(dropdownMenu).addClass('show');
			});

			dropdown.on('mouseleave', function() {
				$(this).removeClass('show')
					.children(dropdownMenu).removeClass('show');
			});
		} else {
			dropdown.off('mouseenter mouseleave');
		}
	}

	$(window).on('resize', adjustNav);

	adjustNav();
});
//New nav



(function ($) {

	"use strict";

	// // Header Type = Fixed NO INFLUENCE
  // $(window).scroll(function() {
  //   var scroll = $(window).scrollTop();
  //   var box = $('.header-text').height();
  //   var header = $('header').height();
  //
  //   if (scroll >= box - header + 15) {
  //     $("header").addClass("background-header");
  //
  //   } else {
  //     $("header").removeClass("background-header");
  //   }
  // });


  // Active
    $(document).on("click", ".naccs .menu div", function() {
      var numberIndex = $(this).index();

      if (!$(this).is("active")) {
          $(".naccs .menu div").removeClass("active");
          $(".naccs ul li").removeClass("active");

          $(this).addClass("active");
          $(".naccs ul").find("li:eq(" + numberIndex + ")").addClass("active");


        }
    });


	$('.owl-listing').owlCarousel({
		items:1,
		loop:true,
		dots: true,
		nav: false,
		autoplay: true,
		margin:30,
		  responsive:{
			  0:{
				  items:1
			  },
			  600:{
				  items:1
			  },
			  1000:{
				  items:1
			  },
			  1600:{
				  items:1
			  }
		  }
	})


	// Menu Dropdown Toggle
  if($('.menu-trigger').length){
    $(".menu-trigger").on('click', function() {
      $(this).toggleClass('active');
      $('.header-area .nav').slideToggle(200);
    });
  }


	// Page loading animation
	 $(window).on('load', function() {

        $('#js-preloader').addClass('loaded');

    });
})(window.jQuery);

 jQuery(function($) {
     $(window).on('scroll', function() {
	 	if ($(this).scrollTop() >= 200) {
	 		$('.navbar').addClass('fixed-top');
	 	} else if ($(this).scrollTop() == 0) {
	 		$('.navbar').removeClass('fixed-top');
	 	}
	 });

 	function adjustNav() {
 		var winWidth = $(window).width(),
 			dropdown = $('.dropdown'),
 			dropdownMenu = $('.dropdown-menu');

 		if (winWidth >= 768) {
 			dropdown.on('mouseenter', function() {
 				$(this).addClass('show')
 					.children(dropdownMenu).addClass('show');
 			});

 			dropdown.on('mouseleave', function() {
 				$(this).removeClass('show')
 					.children(dropdownMenu).removeClass('show');
 			});
 		} else {
 			dropdown.off('mouseenter mouseleave');
 		}
 	}
 	$(window).on('resize', adjustNav);
 	adjustNav();
 });