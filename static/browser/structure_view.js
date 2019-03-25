var structure_view = null;

$(function() {
    structure_view = new Slick.Grid("#structure_view", [], [], options);
    attachAutoResizeDataGrid(structure_view, "structure_view", "tabs_block");
});

function update_structure_view(data) {
    structure_view.setColumns(data.columns);
    structure_view.setData(data.rows);
    structure_view.invalidate();
    structure_view.render();
}