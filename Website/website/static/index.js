// To display age from the slider
var slider = document.getElementById("age");
var output = document.getElementById("out");
output.innerHTML = slider.value;

slider.oninput = function() {
  output.innerHTML = this.value;
}
