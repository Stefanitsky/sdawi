var tree_request_type = 'db_tree';
var tree_get_tables_for_db = ['postgres', 'test'];
var tree_request_JSON = {};

function build_tree_request_JSON() {
	jsonTree = {};
	jsonTree['type'] = tree_request_type;
	jsonTree['get_tables_for_db'] = tree_get_tables_for_db;
	tree_request_JSON = jsonTree;
}

function show_db_tree() {
	$.ajax({
		type: "POST",
		contentType: "application/json; charset=utf-8",
		url: "/get_db_info",
		data: JSON.stringify(tree_request_JSON),
		success: function(data) {
			alert(data);
		},
		dataType: "json"
	});
}