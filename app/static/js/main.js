
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
    stages.forEach(function (item, idx) 
    {
        document.getElementById(`input-1-${item}`).onchange = function() {action(item)} ;
        document.getElementById(`input-2-${item}`).onchange = function() {action(item)} ;
    });
});


function action(game_id) {
    goals1 = document.getElementById(`input-1-${game_id}`).value
    goals2 = document.getElementById(`input-2-${game_id}`).value
    console.log(`${game_id} changed. Score: ${goals1}-${goals2}`)
};