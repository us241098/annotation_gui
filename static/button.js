let buttons = document.getElementsByTagName('button');

let spans = document.getElementsByTagName('span');

for(var i=0; i<buttons.length; i++) {
  buttons[i].addEventListener("click", function(e) {
    let pressed = e.target.getAttribute('aria-pressed') === 'true';
    e.target.setAttribute('aria-pressed', String(!pressed));
  });
}

// span click events since Chrome doesn't trigger button when span is clicked for some reason  -_-;;
for(var i=0; i<spans.length; i++) {
  spans[i].addEventListener("click", function(e) {
    let pressed = e.target.parentElement.getAttribute('aria-pressed') === 'true';
    e.target.parentElement.setAttribute('aria-pressed', String(!pressed));
  });
}
