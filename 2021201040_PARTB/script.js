
$(function(){
  $("#nav").load("nav.html");
});

var slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("dot");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
}
setInterval(function(){ document.getElementById('timer').innerHTML=new Date().toLocaleString();}, 1000);

$(function(){


  //Sample XML    
  var xml = "<?xml version='1.0' ?><doc><person><name>sachin</name><age>21</age></person><person><name>Akash</name><age>18</age></person></doc>";
  
      
  //Parse the givn XML
  var xmlDoc = $.parseXML( xml ); 
      
  var $xml = $(xmlDoc);

  var $person = $xml.find("person");
  
  $person.each(function(){
      
      var name = $(this).find('name').text(),
          age = $(this).find('age').text();
      
      $("#ProfileList" ).append('<li>' +name+ ' - ' +age+ '</li>');
      
  });
          
  });





  // function myfunc() {
  //   var x = document.getElementById('About');
  //   if (x.style.visibility === 'hidden') {
  //     x.style.visibility = 'visible';
  //   } else {
  //     x.style.visibility = 'hidden';
  //   }
  // }