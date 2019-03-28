var tree_requst = new TreeRequest();
var table_request = new TableRequest();
var raw_sql_request = new RawSQLRequest();
var tabs = null;

var sql_input_area = CodeMirror(document.getElementById('sql_input_area'), {
    value: "SELECT * FROM pg_database;",
    mode:  "sql",
    lineNumbers: true,
    autoRefresh: true,
    lineWrapping: true
});

var table_data = new Handsontable(document.getElementById('table_data'), {
    rowHeaders: true,
    colHeaders: true,
    manualRowResize: true,
    manualColumnResize: true,
    contextMenu: true,
    filters: true,
    dropdownMenu: true,
    stretchH: 'all',
    preventOverflow: 'horizontal',
    licenseKey: 'non-commercial-and-evaluation'
});

var raw_sql_result = new Handsontable(document.getElementById('success_sql_result'), {
    rowHeaders: true,
    colHeaders: true,
    manualRowResize: true,
    manualColumnResize: true,
    filters: true,
    dropdownMenu: true,
    stretchH: 'all',
    preventOverflow: 'horizontal',
    licenseKey: 'non-commercial-and-evaluation'
});

$(document).ready(function() {
    // Init jsTree
    $('.db_tree').jstree(
        {'core' : {
            'multiple': false,
            'dblclick_toggle': false,
            'data' : [{'id': 'no_connection', 'parent': '#', 'text': 'No connection'}],
        },
        'plugins' : ['contextmenu']
    });
    // Init tabs
    var tabs = new Tabs({
        elem: "tabs",
        open: 0
    });
    main_tabs_show();
    // Request tree data from the server
    tree_requst.request();
    // Set interval to update every 1 sec
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
        database_tabs_show();
    }
    else if (data.node.a_attr.type == 'table') {
        var db_name = data.node.parent;
        var table_name = data.node.id;
        table_request.update_request_data(db_name, table_name);
        table_request.request();
        table_tabs_show();
    }
    else {
        console.log('Unknown node type');
    }
});

$('.db_tree').on('select_node.jstree', function(e, data) {
    data.instance.open_node(data.node);
});

$('#submit_query').click(function(event) {
    query = sql_input_area.getDoc().getValue();
    raw_sql_request.update_query(query);
    raw_sql_request.request();
});