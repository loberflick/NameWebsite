var loadFile = function(event) {
    var output = document.getElementById('output');
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function() {
        URL.revokeObjectURL(output.src) // free memory
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

