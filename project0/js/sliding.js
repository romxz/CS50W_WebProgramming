// Sliding
function sleep(time) {
    return new Promise((response) => setTimeout(response, time))
}
var aSlides = document.getElementsByClassName("slider-item");
async function slide(iIndex, aSlides) {
    aSlides[iIndex].className = "slider-item active-slider-item";
    if (iIndex == 0) { aSlides[aSlides.length -1].className = "slider-item";
    } else { aSlides[iIndex-1].className = "slider-item";
    }
    sleep(3000).then(() => {
        if (iIndex == aSlides.length-1) { iIndex = -1; }
        slide(iIndex+1, aSlides);
    });
}
slide(0, aSlides);