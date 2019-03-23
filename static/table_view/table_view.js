function build_table_view(container, data) {
    var grid;
    var options = {
        enableCellNavigation: true,
        enableColumnReorder: false
    };
    var headers = {}
    grid = new Slick.Grid("#myGrid", data.rows, data.columns, options);
}