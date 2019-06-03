/** 
 * Create a canvas object of a given width and height. 
 * @param {int} width - The width of the canvas.
 * @param {int} height - The height of the canvas.
 */
function canvas(width = 900, height = 350) {
    var canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    return canvas
}

/** 
 * Render an array of charts within a container. 
 * @param {array} charts_array - Array of chart.js chart data objects.
 * @param {int} container - The container to put them in.
 */
function renderCharts(charts_array, container) {
    for (const i in charts_array) {
        var ctx = canvas()
        var chart = new Chart(ctx.getContext("2d"), charts_array[i])
        container.appendChild(ctx);
    }
}
