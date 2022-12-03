$(document).ready(function () {
    $('#example').DataTable();});
$(document).ready(function () {
    $('#rankings-table').DataTable();});
    $('#rankings-table').dataTable( {
          "lengthChange": false
    } );
$(document).ready(function () {
    $('#predictions-table').DataTable();});
    $('#predictions-table').dataTable( {
          "lengthChange": false
    } );
$(document).ready(function () {
    $('#calendar-table').DataTable();});
    $('#calendar-table').dataTable( {
          "lengthChange": false,
        "ordering": false
    } );
$(document).ready(function () {
    $('#allpredictions-table').DataTable();});
    $('#allpredictions-table').dataTable( {
          "lengthChange": false
    } );


for (const game_id of Array(65).keys()) {
$(document).ready(function () {
    $(`#table_round2_stats_${game_id}`).DataTable();});
    $(`#table_round2_stats_${game_id}`).dataTable( {
        "lengthChange": false,
        "searching": false, 
        "paging": false, 
        "info": false,
        "order": [[0, 'desc']],
    } );
}
