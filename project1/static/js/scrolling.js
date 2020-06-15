// Nav Bar scrolling
window.onscroll = function () {    
    if (document.documentElement.scrollTop > 0) {
        document.getElementById("header").style.backgroundColor = "black";
    } else {
        document.getElementById("header").style.backgroundColor = "transparent";
    };
}