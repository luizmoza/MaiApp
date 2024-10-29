/*--------------  coin_sales4 bar chart start ------------*/
/*--------------  bar chart 08 amchart start ------------*/
if ($('#ambarchart1').length) {
    var chart = AmCharts.makeChart("ambarchart1", {
        "theme": "light",
        "type": "serial",
        "balloon": {
            "adjustBorderColor": false,
            "horizontalPadding": 10,
            "verticalPadding": 20,
            "color": "#fff"
        },
        "dataProvider": [{
            "country": "18/10/20",
            "year2005": 0.223711255519731,
            "year2004": 0.6,
            "color": "#bfbffd",
            "color2": "#7474F0"
        }, {
            "country": "19/10/20",
            "year2005": 0.223711255519731,
            "year2004": 0.6,
            "color": "#bfbffd",
            "color2": "#7474F0"
        }, {
            "country": "20/10/20",
            "year2005": 0.19789569221299,
            "year2004": 0.6,
            "color": "#bfbffd",
            "color2": "#7474F0"
        }, {
            "country": "26/10/20",
            "year2005": 0.193163266576832,
            "year2004": 0.6,
            "color": "#bfbffd",
            "color2": "#7474F0"
        }, {
            "country": "27/10/20",
            "year2005": 0.184160392163725,
            "year2004": 0.6,
            "color": "#bfbffd",
            "color2": "#7474F0"
        }, {
            "country": "28/10/20",
            "year2005": 0.16239205607998,
            "year2004": 0.6,
            "color": "#bfbffd",
            "color2": "#7474F0"
        }, {
            "country": "30/10/20",
            "year2005": 0.303145944435665,
            "year2004": 0.6,
            "color": "#bfbffd",
            "color2": "#7474F0"
        }, {
            "country": "03/11/20",
            "year2005": 0.293550635699158,
            "year2004": 0.6,
            "color": "#bfbffd",
            "color2": "#7474F0"
        }, {
            "country": "06/11/20",
            "year2005": 0.575012874356471,
            "year2004": 0.6,
            "color": "#bfbffd",
            "color2": "#7474F0"
        }, {
            "country": "09/11/20",
            "year2005": 0.6,
            "year2004": 0.6,
            "color": "#bfbffd",
            "color2": "#7474F0"
        }, {
            "country": "10/11/20",
            "year2005": 0.6,
            "year2004": 0.6,
            "color": "#bfbffd",
            "color2": "#7474F0"
        }, {
            "country": "11/11/20",
            "year2005": 0.467772095285341,
            "year2004": 0.6,
            "color": "#bfbffd",
            "color2": "#7474F0"
        }, {
            "country": "13/11/20",
            "year2005": 0.19318032414128,
            "year2004": 0.6,
            "color": "#bfbffd",
            "color2": "#7474F0"
        }, {
            "country": "17/11/20",
            "year2005": 0.118407632611387,
            "year2004": 0.6,
            "color": "#bfbffd",
            "color2": "#7474F0"
        }],
        "valueAxes": [{
            "unit": "%",
            "position": "left",
        }],
        "startDuration": 1,
        "graphs": [{
            "balloonText": "Limite VaR em: <b>[[country]]</b> : <b>[[value]]</b>",
            "fillAlphas": 0.9,
            "fillColorsField": "color",
            "lineAlpha": 0.2,
            "title": "2017",
            "type": "column",
            "valueField": "year2004"
        }, {
            "balloonText": "VaR em: <b>[[country]]</b> : <b>[[value]]</b>",
            "fillAlphas": 0.9,
            "fillColorsField": "color2",
            "lineAlpha": 0.2,
            "title": "2018",
            "type": "column",
            "clustered": false,
            "columnWidth": 0.5,
            "valueField": "year2005"
        }],
        "plotAreaFillAlphas": 0.1,
        "categoryField": "country",
        "categoryAxis": {
            "gridPosition": "start"
        },
        "export": {
            "enabled": false
        }
    });
}