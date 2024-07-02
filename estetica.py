import pandas as pd
import plotly.graph_objects as go

def estetica(figura,x_name = '',y_name = '',title = '',w = 900,h = 450):
    figura.update_xaxes(showgrid=True,showline=True, linewidth=2, linecolor='black', mirror=True,title = x_name)#'cccccccccccccccc')
    figura.update_yaxes(showgrid=True,showline=True, linewidth=2, linecolor='black', mirror=True,title = y_name)


    figura.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor="white",
        template="plotly_white",
        title=title,
        autosize=False,
        width=w,
        height=h,
        #yaxis = dict(range=[0,1]),
        #xaxis = dict(range=[0,1]),
        title_font = dict(size = 20),
        legend=dict(orientation = 'v',
                    font = dict(size = 18),
                     yanchor="top",
                     y=0.99,
                     xanchor="right",
                     x=1,
                     bgcolor='rgba(255,255,255,0.8)',
                   ),
        font = dict(size=20)
    )

def show_with_estetica(x_data, y_data, x_name = '', y_name = '', title = '', w = 1100, h = 450):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines', line=dict(width=5)))
    estetica(fig, x_name, y_name, title, w, h)
    fig.show()

def show_multiple_with_estetica(x_data, y_named_datas, x_name = '', y_name = '', title = '', w = 1200, h = 600):
    fig = go.Figure()
    for y_named_data in y_named_datas:
        y_data, y_data_name = y_named_data
        fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines', name = y_data_name, line=dict(width=5)))
    estetica(fig, x_name, y_name, title, w, h)
    fig.show()