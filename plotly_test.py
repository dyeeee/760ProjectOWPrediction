# import cufflinks
# from mpmath import arange
#
# cufflinks.go_offline(connected=True)
# import chart_studio
# chart_studio.tools.set_credentials_file(username='KexiZhang', api_key='FlQ8axWch9faAuPaNzvj')
# import chart_studio.plotly as py
#
# import plotly.graph_objects as go
#
# trace1 = go.Bar(
#     x = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
#     y = [0.04489641, 0.02152499, 0.05174217, 0.03567577, 0.05253877, 0.05895834,
#          0.04397832, 0.0296181,  0.03787237, 0.04255005, 0.04442705, 0.06093007,
#          0.05984922, 0.06964574, 0.08180381, 0.08038079, 0.08806708, 0.03439907,
#          0.02369489, 0.03744701],
#     name = "testName",
#     marker = dict(color = 'rgb(102,255,255)'),
#     text = "testText")
#
# data = ([trace1])
# py.plot(data, filename='first_start')

# trace0 = go.Bar(
#     x = ['Jan','Feb','Mar','Apr', 'May','Jun',
#          'Jul','Aug','Sep','Oct','Nov','Dec'],
#     y = [20,14,25,16,18,22,19,15,12,16,14,17],
#     name = 'Primary Product',
#     marker=dict(
#         color = 'rgb(49,130,189)'
#     )
# )
# trace1 = go.Bar(
#     x = ['Jan','Feb','Mar','Apr', 'May','Jun',
#          'Jul','Aug','Sep','Oct','Nov','Dec'],
#     y = [19,14,22,14,16,19,15,14,10,12,12,16],
#     name = 'Secondary Product',
#     marker=dict(
#         color = 'rgb(204,204,204)'
#     )
# )
# data = [trace0,trace1]
# py.plot(data, filename='first_start')

RTT = 100
BW = 25  # kB/ms

html_1 = 810
html_1_zip = 57

html_2 = 900
html_2_zip = 75

png_all = 1 + 4 + 3 + 1 + 1 + 1 + 1 + 1
png_noCache = 4 + 3 + 1 + 1 + 1 + 1
max_png = 4

a1 = 2 * RTT + html_1 / BW
a2 = 2 * RTT + html_1 / BW
a3 = 2 * RTT + html_1_zip / BW

a4 = 4 * RTT + html_2 / BW + png_all * 1000 / BW
a5 = 3 * RTT + html_2 / BW + png_all * 1000 / BW
a6 = 3 * RTT + html_2_zip / BW + png_all * 1000 / BW

a7 = 4 * RTT + html_2 / BW + png_noCache * 1000 / BW
a8 = 3 * RTT + html_2 / BW + png_noCache * 1000 / BW
a9 = 3 * RTT + html_2_zip / BW + png_noCache * 1000 / BW

a10 = 2 * RTT + html_2 / BW + 2 * RTT + max_png * 1000 / BW
a11 = 2 * RTT + html_2 / BW + 2 * RTT + max_png * 1000 / BW
a12 = 2 * RTT + html_2_zip / BW + 2 * RTT + max_png * 1000 / BW

print("1: %.2f" % a1)
print("2: %.2f" % a2)
print("3: %.2f" % a3)
print("4: %.2f" % a4)
print("5: %.2f" % a5)
print("6: %.2f" % a6)
print("7: %.2f" % a7)
print("8: %.2f" % a8)
print("9: %.2f" % a9)
print("10: %.2f" % a10)
print("11: %.2f" % a11)
print("12: %.2f" % a12)
