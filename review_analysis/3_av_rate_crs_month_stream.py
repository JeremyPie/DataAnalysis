import justpy as jp
import pandas as pd
from datetime import datetime
from pytz import utc
import matplotlib.pyplot as plt

data = pd.read_csv('reviews.csv', parse_dates = ['Timestamp'])
data['Month'] = data['Timestamp'].dt.strftime('%Y-%m')
month_avg_crs = data.groupby(['Month', 'Course Name'])['Rating'].count().unstack()


chart_def = """
{

    chart: {
        type: 'streamgraph',
        marginBottom: 30,
        zoomType: 'x'
    },

    title: {
        floating: true,
        align: 'left',
        text: 'Winter Olympic Medal Wins',
        x: 20,
        style: {
                    fontSize:'15px'
                }
    },

    xAxis: {
        maxPadding: 0,
        type: 'category',
        crosshair: true,
        categories: [],
        labels: {
            align: 'left',
            reserveSpace: false,
            rotation: 270
        },
        lineWidth: 0,
        margin: 20,
        tickWidth: 0
    },

    yAxis: {
        visible: false,
        startOnTick: false,
        endOnTick: false
    },

    legend: {
        enabled: false
    },

    plotOptions: {
        series: {
            label: {
                minFontSize: 5,
                maxFontSize: 15,
                style: {
                    color: 'rgba(255,255,255,0.75)'
                }
            }
        }
    },

    series: [],

    exporting: {
        sourceWidth: 800,
        sourceHeight: 600
    }

}
"""

def app():
    wp = jp.QuasarPage()

    h1 =  jp.QDiv(a=wp, text = "Analysis of Course Reviews", classes = 'text-h3 text-center q-pt-lg')
    p1 = jp.QDiv(a=wp, text = "These graphs represent course review analysis.", classes = "text-h5 text-center q-pt-md q-pb-lg")
    hc = jp.HighCharts(a=wp, options = chart_def)

    hc.options.title.text = 'Average Rating by Month'
    hc.options.xAxis.categories = list(month_avg_crs.index)
    hc_data = [{'name': v1, 'data': [v2 for v2 in month_avg_crs[v1]]} for v1 in month_avg_crs.columns]
    hc.options.series = hc_data

    return wp

jp.justpy(app)
