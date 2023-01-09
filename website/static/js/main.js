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


let nav = document.querySelector('nav');
let dropdown = nav.querySelector('.dropdown');
let dropdownToggle = nav.querySelector("[data-action='dropdown-toggle']");
let navToggle = nav.querySelector("[data-action='nav-toggle']");

dropdownToggle.addEventListener('click', () => {
	if (dropdown.classList.contains('show')) {
		dropdown.classList.remove('show');
	} else {
		dropdown.classList.add('show');
	}
})

navToggle.addEventListener('click', () => {
	if (nav.classList.contains('opened')) {
		nav.classList.remove('opened');
	} else {
		nav.classList.add('opened');
	}
})