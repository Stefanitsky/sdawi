var tree_request_type = 'db_tree';
var tree_get_tables_for_db = [];
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
			var db_html_tree_block = '';
			$.each(data, function(db_name, db_tables) {
				db_html_tree_block += '<li class="db_name">' + db_name + '</li>';
				if (db_tables.length < 1) return;
				db_html_tree_block += '<ul>';
				$.each(db_tables, function(table_index, table_name) {
					db_html_tree_block += '<li class="table_name">' + table_name + '</li>';
				})
				db_html_tree_block += '</ul>';
			});
			$('.db_list').html(db_html_tree_block);
		},
		dataType: "json"
	});
}

$(document.body).on('click', '.db_name' ,function() {
	var db_name = $(this).closest('li').html();
	if(tree_get_tables_for_db.includes(db_name)) {
       	tree_get_tables_for_db.splice(tree_get_tables_for_db.indexOf(db_name), 1);
   	} else {
   		tree_get_tables_for_db.push(db_name);
   	}
   	show_db_tree();
});