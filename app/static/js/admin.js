
function* range(start, end, step) {
    while (start < end) {
      yield start;
      start += step;
    }
  }

document.addEventListener('DOMContentLoaded', function() 
{
    const first_game_id = parseInt(document.getElementById('first_game_id').value)
    const last_game_id = parseInt(document.getElementById('last_game_id').value) + 1
    let game_ids_to_edit = Array.from(range(first_game_id,last_game_id,1));
    game_ids_to_edit.forEach(function (game_id, idx) 
    {

        document.getElementById(`input-1-${game_id}`).oninput = function() {update_admin_radios(game_id)};
        document.getElementById(`input-2-${game_id}`).oninput = function() {update_admin_radios(game_id)};
        document.getElementById(`radio-1-${game_id}`).onchange   = function() {update_winner(game_id)};
        document.getElementById(`radio-2-${game_id}`).onchange   = function() {update_winner(game_id)};
    });
});
function update_winner(game_id) {
    let radio1 = document.getElementById(`radio-1-${game_id}`);
    let radio2 = document.getElementById(`radio-2-${game_id}`);
    let winner = document.getElementById(`winner-${game_id}`);

    if (radio1.checked) {
        winner.value = radio1.value;
    } else if (radio2.checked) {
        winner.value = radio2.value;
    }
}
    
function update_admin_radios(game_id) {
    let input1 = document.getElementById(`input-1-${game_id}`);
    let input2 = document.getElementById(`input-2-${game_id}`);
    let goals1 = parseInt(input1.value);
    let goals2 = parseInt(input2.value);
    let radio1 = document.getElementById(`radio-1-${game_id}`);
    let radio2 = document.getElementById(`radio-2-${game_id}`);
    let winner = document.getElementById(`winner-${game_id}`);


    if (goals1 >= 0 && goals2 >= 0) {
        radio1.disabled = true;
        radio2.disabled = true;
        if (goals1 > goals2) { //team1 wins
            winner.value = radio1.value;
            radio1.disabled = false;
            radio2.disabled = false;
            radio1.checked = true;
            radio2.checked = false;
            radio1.disabled = true;
            radio2.disabled = true;
            console.log(`goals1: ${radio1.value}${goals1} - ${radio2.value} ${goals2}`)
        } else if (goals1 < goals2) { //team2 wins
            winner.value = radio2.value;
            radio1.disabled = false;
            radio2.disabled = false;
            radio1.checked = false;
            radio2.checked = true;
            radio1.disabled = true;
            radio2.disabled = true;
            console.log(`goals1: ${radio1.value}${goals1} - ${radio2.value} ${goals2}`)
        } else { //tie

            radio1.disabled = false;
            radio2.disabled = false;
        }

    } else {
        radio1.disabled = true;
        radio2.disabled = true;
    }
}