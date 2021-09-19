smallButton = document.getElementById("small");
smallButton.addEventListener("click", makesmall);

largeButton = document.getElementById("large");
largeButton.addEventListener("click", makebig);

function makesmall() {
    Array.from(document.querySelectorAll('.cards')).forEach(function(e) { 
        e.classList.add('small-cards');
        e.classList.remove('large-cards');
    });

    Array.from(document.querySelectorAll('.card')).forEach(function(e) { 
        e.classList.add('small-card');
        e.classList.remove('large-card');
    });
}

function makebig() {
    Array.from(document.querySelectorAll('.cards')).forEach(function(e) { 
        e.classList.remove('small-cards');
        e.classList.add('large-cards');
    });

    Array.from(document.querySelectorAll('.card')).forEach(function(e) { 
        e.classList.remove('small-card');
        e.classList.add('large-card');
    });
  }
  

