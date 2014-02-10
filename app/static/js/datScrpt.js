var urly = "";

function setURLVar (urlstr) {
	urly = urlstr;
}

$(document).ready(function(){
	$("#mainpgCar").carousel("cycle");
	$("#sbar").on("focusin",function(){
		$(this).animate({width: "+=50"},200);
		$(this).prop("placeholder","");
	});
	$("#sbar").on("focusout",function(){
		$(this).animate({width: "-=50"},200);
		$(this).prop("placeholder","Search");
	});
    $('#sbar').keypress(function (e) {
    	if (e.which == 13) {
          window.location = urly + $('#sbar').val();
          return false;
        }
    });
});