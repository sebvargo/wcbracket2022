
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
    49: [1,57], 
    50: [2,57], 
    51: [1,58], 
    52: [2,58], 
    53: [1,59], 
    54: [2,59], 
    55: [1,60], 
    56: [2,60], 
    57: [1,61], 
    58: [2,61], 
    59: [1,62], 
    60: [2,62], 
    61: [1,64], 
    62: [2,64],
}

document.addEventListener('DOMContentLoaded', function() 
{
    stages.forEach(function (game_id, idx) 
    {
        document.getElementById(`input-1-${game_id}`).oninput = function() {update_radios(game_id)};
        document.getElementById(`input-2-${game_id}`).oninput = function() {update_radios(game_id)};
        document.getElementById(`radio-1-${game_id}`).onclick = function() {handle_radios(game_id, 1)};
        document.getElementById(`radio-2-${game_id}`).onclick = function() {handle_radios(game_id, 2)};
    });
});

function update_child(parent_game_id) {
    
    let parent_result = get_radio_result(parent_game_id)
    if (parent_result == 3)  { // in case of tie, look at the radios
        return
    }

    let child_identifier = children[parent_game_id][0] // 1 or 2
    let child_game_id = children[parent_game_id][1] //48, 49 ...64

    let child_label = document.getElementById(`label-${child_identifier}-${child_game_id}`)
    let child_input = document.getElementById(`input-${child_identifier}-${child_game_id}`)
    let child_country = document.getElementById(`country-${child_identifier}-${child_game_id}`)
    // let child_radio = document.getElementById(`radio-${child_identifier}-${child_game_id}`)
    let parent_label = document.getElementById(`label-${parent_result}-${parent_game_id}`).innerHTML
    let parent_country_code = parent_label.split(" ").slice(-1)[0]
    

    child_label.innerHTML = `<img class="align-top" id="img-${child_identifier}-${child_game_id}" src="/static/images/flags/${parent_country_code}.svg" alt="Bootstrap" width="24" height="24">&nbsp; ${parent_country_code}`
    child_input.disabled = false
    child_input.value = ""
    child_country.value = parent_country_code
    
    // handle last two games
    if (child_game_id != 64) {
        update_child(child_game_id)
    } else {
        let loser_result = 0
        if (parent_result == 1 ) {loser_result = 2}
        if (parent_result == 2) {loser_result = 1}

        let loser_parent_label = document.getElementById(`label-${loser_result}-${parent_game_id}`).innerHTML
        let loser_child_label = document.getElementById(`label-${child_identifier}-63`)
        let loser_child_input = document.getElementById(`input-${child_identifier}-63`)
        let loser_country_code = loser_parent_label.split(" ").slice(-1)[0]
        let loser_child_country = document.getElementById(`country-${child_identifier}-63`)
        loser_child_country.value = loser_country_code
        loser_child_label.innerHTML = `<img class="align-top" id="img-${child_identifier}-${child_game_id}" src="/static/images/flags/${loser_country_code}.svg" alt="Bootstrap" width="24" height="24">&nbsp; ${loser_country_code}`
        loser_child_input.disabled = false
    }
}
   

function check_winner(game_id) {
    let goals1 = parseInt(document.getElementById(`input-1-${game_id}`).value)
    let goals2 = parseInt(document.getElementById(`input-2-${game_id}`).value)
    let radio1 = document.getElementById(`radio-1-${game_id}`)
    let radio2 = document.getElementById(`radio-2-${game_id}`)

    if (goals1 != "" && goals2 != "") {
        let result = determine_winner(goals1, goals2, game_id)
        update_radios(result, radio1, radio2)
        console.log(`${game_id}: winner${result}. radio1 ${radio1.checked}, radio 2 ${radio2.checked} `)
        // update_child(game_id, result)
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

function update_radios(game_id) {
    let goals1 = parseInt(document.getElementById(`input-1-${game_id}`).value)
    let goals2 = parseInt(document.getElementById(`input-2-${game_id}`).value)
    let radio1 = document.getElementById(`radio-1-${game_id}`)
    let radio2 = document.getElementById(`radio-2-${game_id}`)
    let country1 = document.getElementById(`country-1-${game_id}`).value
    let country2 = document.getElementById(`country-2-${game_id}`).value
    let winner = document.getElementById(`winner-${game_id}`)
    let runnerup = document.getElementById(`runnerup-${game_id}`)

    if (goals1 != "" && goals2 != "") {
        let result = determine_winner(goals1, goals2, game_id)
        if (result == 1) { //team 1 wins
            radio1.disabled = true
            radio2.disabled = true
            radio1.checked = true
            radio2.checked = false
            radio1.value = 1
            radio2.value = 0
            winner.value = country1
            runnerup.value = country2
            update_child(game_id)
            return 
        } else if (result == 2) { // team 2 wins
            radio1.disabled = true
            radio2.disabled = true
            radio1.checked = false
            radio2.checked = true
            radio1.value = 0
            radio2.value = 1
            winner.value = country2
            runnerup.value = country1
            update_child(game_id)
            return 
        } else { //tie
            radio1.disabled = false
            radio2.disabled = false
            radio1.checked = true
            radio2.checked = false
            radio1.value = 1
            radio2.value = 0
            winner.value = country1
            runnerup.value = country2
            update_child(game_id)
            return 
        }
    } else {
        console.log(`${game_id}: winner CANNOT be determined`)
    }

}

function get_radio_result(game_id) {
    let parent_radio1 = document.getElementById(`radio-1-${game_id}`)
    let parent_radio2 = document.getElementById(`radio-2-${game_id}`)
    if (parent_radio1.checked) { // team1 selected to win
        return 1
    } else if (parent_radio2.checked) {
        return 2
    } else {
        return 3
    }
}

function handle_radios(game_id, radio_num) {
    console.log("changing RADIO")
    let radio1 = document.getElementById(`radio-1-${game_id}`)
    let radio2 = document.getElementById(`radio-2-${game_id}`)

    if (radio_num == 1) {
        radio2.checked = false
        update_child(game_id)
    } else {
        radio1.checked = false
        update_child(game_id)
    }

}



