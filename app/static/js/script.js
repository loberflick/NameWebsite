var loadFile = function(event) {
    var output = document.getElementById('output');
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function() {
        URL.revokeObjectURL(output.src)
    }
};

function closeNav() {
    document.getElementById("sidebar").style.width = "0px";
    document.getElementById("navbar").style.opacity = "0";
}

function openNav() {
    document.getElementById("sidebar").style.width = "350px";
    document.getElementById("navbar").style.opacity = "1";
}

function changeAnswer() {
    for (let i = 1; i < 5; i++){
        if (document.getElementById("select" + String(i)).checked == true){
            document.getElementById("select" + String(i)).parentElement.style.backgroundColor = "#63A46C";
            document.getElementById("select" + String(i)).parentElement.style.borderColor = "Black";
        }
        else {
            document.getElementById("select" + String(i)).parentElement.style.backgroundColor = "#63D471";
            document.getElementById("select" + String(i)).parentElement.style.borderColor = "White";
        }
    }
}
