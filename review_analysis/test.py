import pandas as pd

data = pd.read_csv('reviews.csv', parse_dates = ['Timestamp'])
data['Month'] = data['Timestamp'].dt.strftime('%Y-%m')
month_avg_crs = data.groupby(['Month', 'Course Name']).mean().unstack()


hc_data = [{'name': v1[1], 'data': v2} for v2 in month_avg_crs['Rating'][v1[1]] for v1 in month_avg_crs.columns]
print(hc_data)
