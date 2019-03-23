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
		this.db_names_to_request_tables = [];
		this.request_data['request_tables_list_for_db'] = this.db_names_to_request_tables;
	}

	check_db_name(db_name) {
		if(this.db_names_to_request_tables.includes(db_name)) {
       		this.db_names_to_request_tables.splice(this.db_names_to_request_tables.indexOf(db_name), 1);
   		}
   		else {
   			this.db_names_to_request_tables.push(db_name);
   		}
	}

	// Calls a method that displays the received JSON data as a html tree
	success_request(data) {
		build_db_tree('.db_list', data);
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
		console.log('TableRequest success: ' + data.headers + data.rows);
		build_table_view('#myGrid', data)
	}
}