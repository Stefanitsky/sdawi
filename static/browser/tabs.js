var welcome_tab = $($("#tabs ul").find("li")[0]);
var structure_tab = $($("#tabs ul").find("li")[1]);
var table_data_tab = $($("#tabs ul").find("li")[2]);
var sql_tab = $($("#tabs ul").find("li")[3]);

function main_tabs_show() {
    welcome_tab.show();
    structure_tab.hide();
    table_data_tab.hide();
    sql_tab.show();
    $('div#tabs').tabs("option", "active", 0);
}

function database_tabs_show() {
    welcome_tab.hide();
    structure_tab.show();
    table_data_tab.hide();
    sql_tab.show();
    $('div#tabs').tabs("option", "active", 1);
}

function table_tabs_show() {
    welcome_tab.hide();
    structure_tab.show();
    table_data_tab.show();
    sql_tab.show();
    $('div#tabs').tabs("option", "active", 1);
}