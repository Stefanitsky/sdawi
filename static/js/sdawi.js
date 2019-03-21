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