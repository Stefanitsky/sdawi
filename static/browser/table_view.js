var DATAGRID_MIN_HEIGHT = 100;
var DATAGRID_MIN_WIDTH = 100;
var DATAGRID_BOTTOM_PADDING = 20;
var options = {
        enableCellNavigation: true,
        enableColumnReorder: false,
        forceFitColumns: true
    };
var table_view = null;
$(function() {
    table_view = new Slick.Grid("#table_view", [], [], options);
    attachAutoResizeDataGrid(table_view, "table_view", "tabs_block");
});

/** Attach an auto resize trigger on the datagrid, if that is enable then it will resize itself to the available space
* Options: we could also provide a % factor to resize on each height/width independently
*/
function attachAutoResizeDataGrid(grid, gridId, gridContainerId) {
    var gridDomElm = $('#' + gridId);
    if (!gridDomElm || typeof gridDomElm.offset() === "undefined") {
        // if we can't find the grid to resize, return without attaching anything
        return null;
    }
    //-- 1st resize the datagrid size on first load (because the onResize is not triggered on first page load)
    resizeToFitBrowserWindow(grid, gridId, gridContainerId);
    //-- 2nd attach a trigger on the Window DOM element, so that it happens also when resizing after first load
    $(window).on("resize", function () {
        // for some yet unknown reason, calling the resize twice removes any stuttering/flickering when changing the height and makes it much smoother
        resizeToFitBrowserWindow(grid, gridId, gridContainerId);
        resizeToFitBrowserWindow(grid, gridId, gridContainerId);
    });
    // in a SPA (Single Page App) environment you SHOULD also call the destroyAutoResize()
}

/* destroy the resizer when user leaves the page */
function destroyAutoResize() {
    $(window).trigger('resize').off('resize');
}

/**
* Private function, calculate the datagrid new height/width from the available space, also consider that a % factor might be applied to calculation
* object gridOptions
*/
function calculateGridNewDimensions(gridId, gridContainerId) {
    var availableHeight = $(window).height() - $('#' + gridId).offset().top - DATAGRID_BOTTOM_PADDING;
    var availableWidth = $('#' + gridContainerId).width();
    var newHeight = availableHeight;
    var newWidth = availableWidth;
    // we want to keep a minimum datagrid size, apply these minimum if required
    if (newHeight < DATAGRID_MIN_HEIGHT) {
        newHeight = DATAGRID_MIN_HEIGHT;
    }
    if (newWidth < DATAGRID_MIN_WIDTH) {
        newWidth = DATAGRID_MIN_WIDTH;
    }
    return {
        height: newHeight,
        width: newWidth
    };
}

/** resize the datagrid to fit the browser height & width */
function resizeToFitBrowserWindow(grid, gridId, gridContainerId) {
    // calculate new available sizes but with minimum height of 220px
    var newSizes = calculateGridNewDimensions(gridId, gridContainerId);
    if (newSizes) {
        // apply these new height/width to the datagrid
        $('#' + gridId).height(newSizes.height);
        $('#' + gridId).width(newSizes.width);
        // resize the slickgrid canvas on all browser except some IE versions
        // exclude all IE below IE11
        if (new RegExp('MSIE [6-8]').exec(navigator.userAgent) === null && grid) {
            grid.resizeCanvas();
        }
    }
}

function update_table_view(data) {
    table_view.setColumns(data.columns);
    table_view.setData(data.rows);
    table_view.invalidate();
}