const coordinates = [['top-left','top-middle','top-right'],
                     ['middle-left','middle-middle','middle-right'],
                     ['bottom-left','bottom-middle','bottom-right']];

let moves = [[null,null,null],
             [null,null,null],
             [null,null,null]];


let turn = 'X';
let user = 'X';
let computer = 'O';
let first = false;
let second = true;

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('.col').forEach(box => {
        box.addEventListener('click', (event) => {
            if(turn == user){
                loc = event.target.dataset.location.split(',');
                if(moves[parseInt(loc[0])][parseInt(loc[1])] == null){
                    make_move(loc[0],loc[1]);
                    let str_mat = str_matrix()
                    fetch("/game/status", {
                        method: 'POST',
                        body: JSON.stringify({
                            matrix: str_mat
                        })
                    })
                    .then(response => response.json())
                    .then(match => {
                        if(match.end){
                            switch (match.winner) {
                                case 'X':
                                    alert("X wins");
                                    document.querySelector(".restart").style.display = "block";
                                    break;
                                case 'O':
                                    alert("O wins");
                                    document.querySelector(".restart").style.display = "block";
                                    break;
                                default:
                                    alert("Match Draw");
                                    document.querySelector(".restart").style.display = "block";
                                    break;
                            }
                        }
                        else{
                            turn = computer;
                            ai_play();
                        }
                    });
                }
                else{
                    console.log("Not Allowed");
                }
            }
        });
    });
    document.querySelector(".selector .start-btn").onclick = () => {
        document.querySelector('.sign-choice').style.display = 'none';
        document.querySelector('.game').style.display = 'block';
        if(first){
            ai_play();
        }
    };
    document.querySelectorAll(".draw").forEach((btn) => {
        btn.addEventListener("click", (event) => {
            event.target.parentElement.parentElement.querySelector("input[type='radio']").checked = true;
            event.target.classList.add("selected");
            switch (event.target.id) {
                case "x":
                    document.querySelector("#o").classList.remove("selected");
                    user = "X";
                    computer = "O";
                    first = false;
                    second = true;
                    break;
                case "o":
                    document.querySelector("#x").classList.remove("selected");
                    user = "O";
                    computer = "X";
                    first = true;
                    second = false;
                    break;
                default:
                    break;
            }
        });
    });
});

function ai_play(){
    if(first){
        setTimeout(() => {
            i = Math.floor(Math.random()*2.99);
            j = Math.floor(Math.random()*2.99);
            make_move(i,j);
            turn = user;
            first = false;
        },600);
        return;
    }
    else if(second){
        ai_turn();
        second = false;
    }
    else{
        setTimeout(() =>{
            ai_turn();
        },500);
    }
}

function ai_turn(){
    let str_mat = str_matrix()
    fetch("/game/move", {
        method: 'POST',
        body: JSON.stringify({
            matrix: str_mat
        })
    })
    .then(response => response.json())
    .then(move => {
        make_move(move.row,move.col);
    })
    .then(() => {
        str_mat = str_matrix()
        fetch("/game/status", {
            method: 'POST',
            body: JSON.stringify({
                matrix: str_mat
            })
        })
        .then(response => response.json())
        .then(match => {
            if(match.end){
                switch (match.winner) {
                    case 'X':
                        alert("X wins");
                        document.querySelector(".restart").style.display = "block";
                        break;
                    case 'O':
                        alert("O wins");
                        document.querySelector(".restart").style.display = "block";
                        break;
                    default:
                        alert("Match Draw");
                        document.querySelector(".restart").style.display = "block";
                        break;
                }
            }
            else{
                turn = user;
            }
        });
    });
}

function make_move(i,j){
    moves[parseInt(i)][parseInt(j)] = turn;
    document.querySelector(`.${coordinates[parseInt(i)][parseInt(j)]}`).innerHTML = `<span>${turn}</span>`;
}


function str_matrix(){
    matrix = "";
    for (let i = 0; i < moves.length; i++) {
        for (let j = 0; j < moves[i].length; j++) {
            if (moves[i][j] == null) {
                matrix = matrix.concat(0);
            }
            else{
                matrix = matrix.concat(moves[i][j]);
            }
        }
    }
    return matrix;
}
