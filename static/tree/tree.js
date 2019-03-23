function build_db_tree(container, data) {
	// var db_html_tree_block = '';
	// $.each(data, function(db_name, db_tables) {
	// 	db_html_tree_block += '<li class="db_name">' + db_name + '</li>';
	// 	if (db_tables.length < 1) return;
	// 	db_html_tree_block += '<ul>';
	// 	$.each(db_tables, function(table_index, table_name) {
	// 		db_html_tree_block += '<li class="table_name">' + table_name + '</li>';
	// 	})
	// 	db_html_tree_block += '</ul>';
	// });
	// $(container).html(db_html_tree_block);
	$('.db_tree').jstree(
		{ 'core' : {
	    'data' : [
	       { "id" : "postgres", "parent" : "#", "text" : "postgres" },
	       { "id" : "test1", "parent" : "#", "text" : "test" },
	       { "id" : "test2", "parent" : "#", "text" : "test" },
	       { "id" : "test3", "parent" : "#", "text" : "test" },
	       { "id" : "friends", "parent" : "postgres", "text" : "fiends"}
	    ]
	}});
}