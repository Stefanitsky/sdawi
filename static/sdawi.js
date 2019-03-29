// Request initialisation
var tree_requst = new TreeRequest();
var table_data_request = new TableDataRequest();
var raw_sql_request = new RawSQLRequest();
var table_structure_request = new TableStructureRequest();
var db_structure_request = new DatabaseStructureRequest();
// Create tabs variable
var tabs = null;
// SQL input area initialisation
var sql_input_area = CodeMirror(document.getElementById('sql_input_area'), {
    value: "SELECT * FROM pg_database;",
    mode:  "sql",
    lineNumbers: true,
    autoRefresh: true,
    lineWrapping: true
});
// Table for data display initialisation
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
// Table for success sql request display initialisation
var raw_sql_result = new Handsontable(document.getElementById('success_sql_result'), {
    rowHeaders: true,
    colHeaders: true,
    manualRowResize: true,
    manualColumnResize: true,
    filters: true,
    dropdownMenu: true,
    stretchH: 'all',
    preventOverflow: 'horizontal',
    height: 500,
    licenseKey: 'non-commercial-and-evaluation'
});
// Table for db/table structure display initialisation
var structure_data = new Handsontable(document.getElementById('structure_data'), {
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
// Initialisation on document ready (after page loads)
$(document).ready(function() {
    // Init jsTree
    $('.db_tree').jstree(
        {'core' : {
            'multiple': false,
            'dblclick_toggle': false,
            'data': [
                {'id': 'no_connection',
                    'parent': '#',
                    'text': 'No connection',
                    'a_attr': {
                        'type': 'host'
                    }
                }
            ],
        },
        //'plugins' : ['types']
    });
    // Init tabs
    tabs = new Tabs({
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
// Add events on activate node
$('.db_tree').on('activate_node.jstree', function (e, data) {
    if (data.node.a_attr.type == 'host') {
        main_tabs_show();
    }
    if (data.node.a_attr.type == 'db') {
        tree_requst.add_db_name(data.node.id);
        tree_requst.request();
        db_structure_request.update_request_data(data.node.id);
        db_structure_request.request();
        database_tabs_show();

    }
    else if (data.node.a_attr.type == 'table') {
        var db_name = data.node.parent;
        var table_name = data.node.id;
        table_data_request.update_request_data(db_name, table_name);
        table_data_request.request();
        table_structure_request.update_request_data(db_name, table_name);
        table_structure_request.request();
        table_tabs_show();
    }
    else {
        console.log('Unknown node type');
    }
});
// Add events on select node
$('.db_tree').on('select_node.jstree', function(e, data) {
    data.instance.open_node(data.node);
});
// Add events on click of the submit query button
$('#submit_query').click(function(event) {
    query = sql_input_area.getDoc().getValue();
    raw_sql_request.update_query(query);
    raw_sql_request.request();
});