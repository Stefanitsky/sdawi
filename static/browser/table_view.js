class TableView {
    constructor(table_view_id, columns, rows) {
        // Defaults
        this.options = {
            enableCellNavigation: true,
            enableColumnReorder: false,
            forceFitColumns: true
        };
        // Creating grid
        this.table_view_id = table_view_id;
        this.grid = new Slick.Grid('#' + this.table_view_id, 
            columns, rows, this.options);
    }

    update_data(columns, rows) {
        this.grid.setColumns(columns);
        this.grid.setData(rows);
        this.grid.invalidate();
    }
}