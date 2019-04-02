/*
* Global values for each tab
*/
var welcome_tab = $($("#tabs ul").find("li")[0]);
var structure_tab = $($("#tabs ul").find("li")[1]);
var table_data_tab = $($("#tabs ul").find("li")[2]);
var sql_tab = $($("#tabs ul").find("li")[3]);

/*
* Functions for managing tabs.
*/

// Returns the Raw SQL tab to its original state
function load_sql_tab() {
    $('#error_sql_result').hide();
    $('#success_sql_result').hide();
    sql_tab.show();
}

// Hides unnecessary tabs on the main page when the user is logged in
function main_tabs_show() {
    welcome_tab.show();
    structure_tab.hide();
    table_data_tab.hide();
    load_sql_tab();
    tabs.open(0);
}

// Hides unnecessary tabs when selecting a database
function database_tabs_show() {
    welcome_tab.hide();
    structure_tab.show();
    table_data_tab.hide();
    sql_tab.show();
    tabs.open(1);
}

// Hides unnecessary tabs when selecting a table
function table_tabs_show() {
    welcome_tab.hide();
    structure_tab.show();
    table_data_tab.show();
    sql_tab.show();
    tabs.open(1);
}

// Returns the Raw SQL tab to its original state when it was clicked
sql_tab.click(function(event) {
    load_sql_tab();
});