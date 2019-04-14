/*
* Global values for each tab
*/
var welcome_tab = $('#browser-tabs a[id="nav-welcome-tab"]');
var structure_tab = $('#browser-tabs a[id="nav-structure-tab"]');
var table_data_tab = $('#browser-tabs a[id="nav-data-tab"]');
var sql_tab = $('#browser-tabs a[id="nav-sql-tab"]');

/*
* Functions for managing tabs.
*/

// Returns the Raw SQL tab to its original state
function load_sql_tab() {
    $('#sql_result').hide();
    $('#sql_data').hide();
    sql_tab.show();
    resize_sql_result_table();
}

// Hides unnecessary tabs on the main page when the user is logged in
function main_tabs_show() {
    welcome_tab.show();
    structure_tab.hide();
    table_data_tab.hide();
    load_sql_tab();
    welcome_tab.tab('show');
}

// Hides unnecessary tabs when selecting a database
function database_tabs_show() {
    welcome_tab.hide();
    structure_tab.show();
    table_data_tab.hide();
    sql_tab.show();
    structure_tab.tab('show');
}

// Hides unnecessary tabs when selecting a table
function table_tabs_show() {
    welcome_tab.hide();
    structure_tab.show();
    table_data_tab.show();
    sql_tab.show();
    table_data_tab.tab('show');
}

/*
*  Tabs click events
*/

// Returns the Raw SQL tab to its original state when it was clicked
sql_tab.click(function(event) {
    load_sql_tab();
});
// Structure tab click event
structure_tab.click(function(event) {
    resize_structure_table();
});
// Table data tab click event
table_data_tab.click(function(event) {
    resize_data_table();
});
