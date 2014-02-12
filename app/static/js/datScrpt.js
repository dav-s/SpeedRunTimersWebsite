
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
});