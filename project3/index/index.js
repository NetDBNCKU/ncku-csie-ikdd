/*global d3: false, Firebase: false, $:false */

(function () {
    'use strict';
    var svg,
        xScale,
        yScale,
        pointColor,
        data = [],
        ref;
    ref = new Firebase("https://burning-fire-3884.firebaseio.com/game");
    ref.once('value', function (snapshot) {
        data = snapshot.val();
    
        // Points
        pointColor = d3.scale.category20b();
        d3.select('svg g.chart')
            .selectAll('circle')
            .data(data)
            .enter()
            .append('circle')
            .attr('cx', function (d) {
                return xScale(new Date(d.time * 1000));
            })
            .attr('cy', function (d) {
                return yScale(Math.log10(d.view));
            })
            .attr('r', 2)
            .attr('fill', function (d) {
                return pointColor(d.platform);
            });
        
        $('div.mdl-spinner').remove();
        
        // Options
    });
    svg = d3.select('#plot')
            .append('svg')
            .attr('width', '1000px')
            .attr('height', '640px');
    svg.append('g').classed('chart', true).attr('transform', 'translate(90, -40)');
    
    // Axis labels
    d3.select('svg g.chart')
        .append('text')
        .attr({'id': 'xLabel', 'x': 450, 'y': 670})
        .text('時間');
    d3.select('svg g.chart')
        .append('text')
        .attr('id', 'yLabel')
        .attr('transform', 'translate(-75, 330) rotate(-90)')
        .text('瀏覽');
    
    // Axis scales
    xScale = d3.time.scale().domain([new Date(343260800 * 1000), new Date(1481881600 * 1000)]).range([20, 880]);
    yScale = d3.scale.linear().domain([Math.log10(100), Math.log10(2600000)]).range([600, 100]);
    d3.select('svg g.chart')
        .append('g')
        .attr('transform', 'translate(0, 630)')
        .attr('id', 'xAxis');
    d3.select('svg g.chart g#xAxis')
        .call(d3.svg.axis()
             .scale(xScale)
             .orient('bottom'));
    d3.select('svg g.chart')
        .append('g')
        .attr('transform', 'translate(5, 0)')
        .attr('id', 'yAxis');
    d3.select('svg g.chart g#yAxis')
        .call(d3.svg.axis()
             .scale(yScale)
             .orient('left'));
    
    $('body').append('<div class="mdl-spinner mdl-js-spinner is-active"></div>');
    d3.select('div.mdl-spinner')
        .attr('id', 'spinner');
}());

function try_func() {
    d3.select('svg g.chart')
        .selectAll('circle')
        .attr('r', function (d) {
            console.log(d.platform + '\n');
            return 2;
        });
}
