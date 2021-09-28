import justpy as jp
import pandas as pd
from datetime import datetime
from pytz import utc
import matplotlib.pyplot as plt

data = pd.read_csv('reviews.csv', parse_dates = ['Timestamp'])
data['Day'] = data['Timestamp'].dt.date
day_average = data.groupby(['Day']).mean()


chart_def = """
{
    chart: {
        type: 'spline',
        inverted: false
    },
    title: {
        text: 'Atmosphere Temperature by Altitude'
    },
    subtitle: {
        text: ''
    },
    xAxis: {
        reversed: false,
        title: {
            enabled: true,
            text: 'Date'
        },
        labels: {
            format: '{value}'
        },
        accessibility: {
            rangeDescription: 'Range: 0 to 80 km.'
        },
        maxPadding: 0.05,
        showLastLabel: true
    },
    yAxis: {
        title: {
            text: 'Average Rating'
        },
        labels: {
            format: '{value}'
        },
        accessibility: {
            rangeDescription: 'Range: -90°C to 20°C.'
        },
        lineWidth: 2
    },
    legend: {
        enabled: false
    },
    tooltip: {
        headerFormat: '<b>{series.name}</b><br/>',

        pointFormat: '{point.x}: {point.y} stars'
    },
    plotOptions: {
        spline: {
            marker: {
                enable: false
            }
        }
    },
    series: [{
        name: 'Average Rating',
        data: [[0, 15], [10, -50], [20, -56.5], [30, -46.5], [40, -22.1],
            [50, -2.5], [60, -27.7], [70, -55.7], [80, -76.5]]
    }]
}
"""
async def tooltip_formatter(self, msg):
    d1 = jp.Div(text=msg.series_name, style=f'color: blue;')
    d2 = jp.Div(text=f'Date: {msg.category}')
    d3 = jp.Div(text=f'Avg Rating: {msg.y}')
    tooltip_html = d1.to_html() + d2.to_html() + d3.to_html()
    return await self.tooltip_update(tooltip_html, msg.websocket)

def app():
    wp = jp.QuasarPage()

    h1 =  jp.QDiv(a=wp, text = "Analysis of Course Reviews", classes = 'text-h3 text-center q-pad-md')
    p1 = jp.QDiv(a=wp, text = "These graphs represent course review analysis.")
    hc = jp.HighCharts(a=wp, options = chart_def)
    hc.options.title.text = 'Average Rating by Day'
    hc.options.xAxis.categories = list(day_average.index)
    hc.options.series[0].data = list(day_average['Rating'])
    hc.on('tooltip', tooltip_formatter)
    return wp

jp.justpy(app)
