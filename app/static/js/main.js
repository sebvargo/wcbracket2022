
const stages = [49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64]


parents = {
    57: [49, 50],
    58: [51, 52],
    59: [53, 54],
    60: [55, 56],
    61: [57, 58],
    62: [59, 60],
    63: [61, 62],
    64: [61, 62],
}

children = {
    49: 57, 
    50: 57, 
    51: 58, 
    52: 58, 
    53: 59, 
    54: 59, 
    55: 60, 
    56: 60, 
    57: 61, 
    58: 61, 
    59: 62, 
    60: 62, 
    61: 63, 
    62: 63
}


document.addEventListener('DOMContentLoaded', function() 
{
    stages.forEach(function (game_id, idx) 
    {
        document.getElementById(`input-1-${game_id}`).oninput = function() {check_winner(game_id)} ;
        document.getElementById(`input-2-${game_id}`).oninput = function() {check_winner(game_id)} ;
        document.getElementById(`radio-1-${game_id}`).onclick = function() {handle_radios(game_id, 1)};
        document.getElementById(`radio-2-${game_id}`).onclick = function() {handle_radios(game_id, 2)};
    });
});


function check_winner(game_id) {
    let goals1 = parseInt(document.getElementById(`input-1-${game_id}`).value)
    let goals2 = parseInt(document.getElementById(`input-2-${game_id}`).value)
    let radio1 = document.getElementById(`radio-1-${game_id}`)
    let radio2 = document.getElementById(`radio-2-${game_id}`)

    if (goals1 != "" && goals2 != "") {
        let result = determine_winner(goals1, goals2, game_id)
        update_radios(result, radio1, radio2)
        console.log(`${game_id}: winner${result}. radio1 ${radio1.checked}, radio 2 ${radio2.checked} `)

    } else {
        console.log(`${game_id}: winner CANNOT be determined`)
    }
};

function determine_winner(goals1, goals2) {
    // returns 1 if team1, 2 if team2 and 3 if tie
    if (goals1 > goals2) { //team 1 wins
        return 1
    } else if (goals1 < goals2) { // team 2 wins
        return 2
    } else { //tie
        return 3 // tie
    }
}

function update_radios(result, radio1, radio2) {
    if (result == 1) { //team 1 wins
        radio1.disabled = true
        radio2.disabled = true
        radio1.checked = true
        radio2.checked = false
        return
    } else if (result == 2) { // team 2 wins
        radio1.disabled = true
        radio2.disabled = true
        radio1.checked = false
        radio2.checked = true
        return
    } else { //tie
        radio1.disabled = false
        radio2.disabled = false
        radio1.checked = false
        radio2.checked = false
        return 
    }
}

function handle_radios(game_id, radio_num) {
    console.log(radio_num)
    let radio1 = document.getElementById(`radio-1-${game_id}`)
    let radio2 = document.getElementById(`radio-2-${game_id}`)

    if (radio_num == 1) {
        radio2.checked = false
    } else {
        radio1.checked = false
    }
}