let gameBoardForm = document.getElementById("gameBoardForm");

// for (let i = 0; i < 100; i++) {
//     let gridBox = document.createElement("button");
//     gridBox.setAttribute("type", "submit");
//     gridBox.setAttribute("class", "gridBox");
//     gridBox.setAttribute("name", "gridBox");
//     gridBox.setAttribute("value", i);
//     gridBox.addEventListener("mousedown", flagClick);
//     gridBox.addEventListener('contextmenu', event => event.preventDefault());
//     gameBoardForm.appendChild(gridBox);
// }

let gridRects = document.getElementsByTagName("button");
gridRects = Array.from(gridRects); // turns htmlCollection into array

gridRects.forEach(button => {
    button.addEventListener("mousedown", flagClick);
    button.addEventListener('contextmenu', event => event.preventDefault()); // remove right click menu
});

for (let i = 100; i < 200; i++) {
    let gridBox = document.createElement("button");
    gridBox.setAttribute("type", "submit");
    gridBox.setAttribute("class", "hidden_flag_button");
    gridBox.setAttribute("name", "gridBox");
    gridBox.setAttribute("value", i);
    gameBoardForm.appendChild(gridBox);
}

let flags = document.getElementsByClassName("hidden_flag_button");

function flagClick(e) {
    if (e.which == 3) {
        flags[this.value].click();
    }
}