var tree_requst = new TreeRequest();

$(document).ready(function() {
    $('.db_tree').jstree(
        {'core' : {
            'multiple': false,
            'dblclick_toggle': false,
            'data' : [{'id': 'no_connection', 'parent': '#', 'text': 'No connection'}],
        },
        'plugins' : ['contextmenu']
    });
    $("div#tabs_block").tabs();
    tree_requst.request();
	setInterval(function() {
	 		tree_requst.request();
	 	}, 
	 	1000
	);
});


$('.db_tree').on('activate_node.jstree', function (e, data) {
    if (data.node.a_attr.type == 'db') {
        tree_requst.add_db_name(data.node.id);
        tree_requst.request();
    }
    else if (data.node.a_attr.type == 'table') {
        var table_request = new TableRequest();
        var db_name = data.node.parent;
        var table_name = data.node.id;
        table_request.update_request_data(db_name, table_name);
        table_request.request();
    }
    else {
        console.log('Unknown node type');
    }
});

$('.db_tree').on('select_node.jstree', function(e, data) {
    data.instance.open_node(data.node);
});
