var tree_requst = new TreeRequest();
var data = null;


$(document).ready(function() {
	setInterval(function() {
			tree_requst.request();
		}, 
		1000
	);
});


$(document.body).on('click', '.db_name' ,function() {
	var db_name = $(this).closest('li').html();
 	tree_requst.check_db_name(db_name);
   	tree_requst.request();
});

// TODO: db_name parse
$(document.body).on('click', '.table_name' ,function() {
	var table_name = $(this).closest('li').html();
    var db_name = $(this).parent('ul').html();
    console.log(db_name);
   	var table_request = new TableRequest();
    table_request.update_request_data(db_name, table_name);
   	table_request.request();
});

$('.db_tree').on("activate_node.jstree", function (e, data) {
  console.log(data.node.id);
});