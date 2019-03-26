/**
* Base request class
*/
class RequestData {
	// Automatically called when creating an instance,
	// saves request type, request data (basic, contains only type) and data
	constructor(request_type) {
		this.request_type = request_type;
		this.request_data = {type: request_type};
		this.data = null;
	}

	// Sends an ajax post request to the server,
	// and calls success_request() method if the request was successful
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

	// Performs the necessary actions on the data
	success_request(data) {
		console.log('success_request() not implemented!');
	}

	fail_request(data) {
		console.log('fail_request() not implemented!');
	}
}

/**
* Tree request class, extends base request class (RequestData)
*/
class TreeRequest extends RequestData {
	constructor() {
		super('db_tree');
		this.request_tables_list_for_db = [];
		this.request_data['request_tables_list_for_db'] = this.request_tables_list_for_db;
	}

	remove_db_name(db_name) {
		if (!this.request_tables_list_for_db.includes(db_name)) return;
		this.request_tables_list_for_db.splice(this.request_tables_list_for_db.indexOf(db_name), 1);
	}

	add_db_name(db_name) {
		if (this.request_tables_list_for_db.includes(db_name)) return;
		this.request_tables_list_for_db.push(db_name);
	}

	// Action on success request
	success_request(data) {
		var jsTreeData = JSON.stringify($('.db_tree').jstree(true).settings.core.data);
		if (jsTreeData !== JSON.stringify(data)) {
			$('.db_tree').jstree(true).settings.core.data = data;
			$('.db_tree').jstree(true).refresh();
		}
	}

	fail_request(data) {
		console.log('TreeRequest fail: ' + data);
	}
}

/**
* Table request class, extends base request class (RequestData)
*/
class TableRequest extends RequestData {
	constructor() {
		super('table_data');
	}

	update_request_data(db_name, table_name) {
		this.request_data['db_name'] = db_name;
		this.request_data['table_name'] = table_name;
	}

	success_request(data) {
		table_view.update_data(data.columns, data.rows);
	}

	fail_request(data) {
		console.log('TableRequest fail: ' + data);
	}
}

class RawSQLRequest extends RequestData {
	constructor() {
		super('raw_sql');
	}

	update_query(query) {
		this.request_data['query'] = query;
	}

	success_request(data) {
		if ('error' in data) {
			console.log('OOPSIEE' + data.error);
		} else {
			console.log('RawSQLRequest success: ' + data);
		}
	}

	fail_request(data) {
		console.log('RawSQLRequest fail: ' + data);
	}
}