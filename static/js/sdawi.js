$(document).ready(function() {
	build_tree_request_JSON();
	show_db_tree();
	setInterval(function() {
		build_tree_request_JSON();
		show_db_tree();
		}, 
		1000
	);
});

// $(document.body).on('click', '.db_name' ,function() {
// 	var db_name = $(this).closest('a').html();
// 	db_table_list = show_db_tables($(this).closest('a'));
// });