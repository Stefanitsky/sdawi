/**
* Base request class.
*/
class RequestData {
	// Automatically called when creating an instance,
	// saves request type, request data (basic, contains only type) and data.
	constructor(request_type) {
		this.request_data = {}
		this.request_data['type'] = request_type;
		this.data = null;
	}

	// Sends an ajax post request to the server,
	// and calls success_request() method if the request was successful,
	// or calls fail_request() method if the request caused an error.
	request() {
		$.ajax({
			type: "POST",
			contentType: "application/json; charset=utf-8",
			url: "/get_db_info",
			data: JSON.stringify(this.request_data),
			success: data => this.success_request(data),
			error: data => this.fail_request(data),
			dataType: "json"
		});
	}

	// Performs the necessary actions on the data upon a successful request
	success_request(data) {
		console.error('success_request() not implemented!');
	}

	// Performs the necessary actions on the data in case of a failed request
	fail_request(data) {
		console.error('fail_request() not implemented!');
	}
}

/**
* Tree request class, extends base request class (RequestData).
* Requests the database tree and performs the necessary actions when responding.
*/
class TreeRequest extends RequestData {
	constructor() {
		super('db_tree');
		this.request_tables_list_for_db = [];
		this.request_data['request_tables_list_for_db'] = this.request_tables_list_for_db;
	}

	// Removes db name from the request
	remove_db_name(db_name) {
		if (!this.request_tables_list_for_db.includes(db_name)) return;
		this.request_tables_list_for_db.splice(this.request_tables_list_for_db.indexOf(db_name), 1);
	}

	// Adds db name to the request
	add_db_name(db_name) {
		if (this.request_tables_list_for_db.includes(db_name)) return;
		this.request_tables_list_for_db.push(db_name);
	}

	// Updates the data in the jsTree upon successful request
	success_request(data) {
		var jsTreeData = JSON.stringify($('.db_tree').jstree(true).settings.core.data);
		if (jsTreeData !== JSON.stringify(data)) {
			$('.db_tree').jstree(true).settings.core.data = data;
			$('.db_tree').jstree(true).refresh();
		}
	}

	fail_request(data) {
		console.error('TreeRequest fail: ' + data);
	}
}

/**
* Table request class, extends base request class (RequestData).
* Requests the table data and performs the necessary actions when responding.
*/
class TableDataRequest extends RequestData {
	constructor() {
		super('table_data');
	}

	// Updates the db name and table name for the request
	update_request_data(db_name, table_name) {
		this.request_data['db_name'] = db_name;
		this.request_data['table_name'] = table_name;
	}

	// Update data in the data table upon successful request
	success_request(data) {
		table_data.updateSettings({
			colHeaders: data.colHeaders,
			columns: data.columns,
			data: data.rows
		});
	}

	fail_request(data) {
		console.error('TableRequest fail: ' + data);
	}
}

/**
* Raw SQL request class, extends base request class (RequestData).
* Requests the data as table by raw sql and performs the necessary actions when responding.
*/
class RawSQLRequest extends RequestData {
	constructor() {
		super('raw_sql');
	}

	// Updates query for the request
	update_query(query) {
		this.request_data['query'] = query;
	}

	// Updates the db name for which the query is intended
	update_selected_db(selected_db) {
		this.request_data['selected_db'] = selected_db;
	}

	// Displays a table with data or error alert
	success_request(data) {
		if ('error' in data) {
			$('#success_sql_result').hide();
			var alert = '<div class="alert alert-danger" role="alert">';
			alert += data.error + '</div>';
			$('#error_sql_result').html(alert);
			$('#error_sql_result').show();
		} else {
			$('#error_sql_result').hide();
			$('#success_sql_result').show();
			raw_sql_result.updateSettings({
				colHeaders: data.colHeaders,
				columns: data.columns,
				data: data.rows
			});
		}
	}

	fail_request(data) {
		console.error('RawSQLRequest fail: ' + data);
	}
}

/**
* Table structure request class, extends base request class (RequestData).
* Requests the table structure data and performs the necessary actions when responding.
*/
class TableStructureRequest extends RequestData {
	constructor() {
		super('table_structure');
	}

	// Updates db and table name for the request
	update_request_data(db_name, table_name) {
		this.request_data['db_name'] = db_name;
		this.request_data['table_name'] = table_name;
	}

	// Updates structure data of the table upon successful request
	success_request(data) {
		structure_data.updateSettings({
			colHeaders: data.colHeaders,
			columns: data.columns,
			data: data.rows
		});
	}

	fail_request(data) {
		console.error('TableStructureRequest fail: ' + data);
	}
}

/**
* Database structure request class, extends base request class (RequestData).
* Requests the db structure data and performs the necessary actions when responding.
*/
class DatabaseStructureRequest extends RequestData {
	constructor() {
		super('database_structure');
	}

	// Updates db name for the request
	update_request_data(db_name) {
		this.request_data['db_name'] = db_name;
	}

	// Updates db data of the table upon successful request
	success_request(data) {
		structure_data.updateSettings({
			colHeaders: data.colHeaders,
			columns: data.columns,
			data: data.rows
		});
	}

	fail_request(data) {
		console.error('DatabaseStructureRequest fail: ' + data);
	}
}