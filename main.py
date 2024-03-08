import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import numpy as np
import Gmake as Gmake

#初始化
app = dash.Dash(__name__)
#添加布局和按钮
app.layout = html.Div([
    dcc.Graph(id='Screen',style={'width': '1000px', 'height': '1000px'}),
    html.Button('Random_Point', id='gen-point-button', n_clicks=0),
    html.Button('Random Line', id='gen-line-button', n_clicks=0),
    html.Button('Dijktsra', id='dijkstra-solve', n_clicks=0),
    html.Button("RESET",id='clear-screen',n_clicks=0)
])
#定义槽与信号
@app.callback(
    Output('Screen', 'figure'),
    [Input('gen-point-button', 'n_clicks'),
     Input('clear-screen', 'n_clicks'),
     Input('gen-line-button','n_clicks'),
     Input('dijkstra-solve','n_clicks')]
)
def update_figure(a,b,c,d):
    global random_point_x,random_point_y,fig,layout,line_trace,scatter_trace,gragh,path_trace
    #处理信号
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    #针对不同信号的处理
    if button_id == 'gen-point-button':
        random_point_x+=np.random.uniform(0,100 ,10).tolist()
        random_point_y += np.random.uniform(0, 100, 10).tolist()
        scatter_trace = go.Scatter(
            x=random_point_x,
            y=random_point_y,
            mode='markers',
            marker=dict(
                color='blue',
                size=10,
                opacity=0.8,
            )
        )
        fig = go.Figure(data=[scatter_trace,line_trace], layout=layout)
        return fig
    elif button_id=='gen-line-button':
        gragh,traces=Gmake.gragh_sprase(random_point_x,random_point_y,len(random_point_x)//2-1)
        fig = go.Figure(data=[scatter_trace], layout=layout)
        for trace in traces:
            fig.add_trace(trace)
        fig.update_layout(title='Layer={}'.format(len(random_point_x)//2), showlegend=False)
        return fig
    elif button_id == 'dijkstra-solve':
        path=Gmake.dijkstra_path(gragh,0,1)
        path_x,path_y=Gmake.line_bypath(path,random_point_x,random_point_y)
        fig.add_trace(go.Scatter(
            x=path_x,
            y=path_y,
            mode='lines',
            line=dict(
                color='red',
                width=2,
                dash='solid',
                )
            )
        )
        fig.update_layout(title='Layer={}'.format(len(random_point_x) // 2), showlegend=False)
        return fig
    elif button_id == 'clear-screen':
        random_point_x=[2,98]
        random_point_y=[2,98]
        line_trace = go.Scatter()
        gragh={}
        path_trace=go.Scatter()
        fig = go.Figure(data=None, layout=layout)
        return fig
    #默认返回
    else:
        return fig

if __name__ == '__main__':
    random_point_x = [2, 98]
    random_point_y = [2, 98]
    layout = go.Layout(
        title='Random Point',
        xaxis=dict(range=[0, 100], autorange=False),
        yaxis=dict(range=[0, 100], autorange=False),
        showlegend=False
    )
    scatter_trace = go.Scatter(
        x=random_point_x,
        y=random_point_y,
        mode='markers',
        marker=dict(
            color='blue',
            size=10,
            opacity=0.8,
        ),
    )
    line_trace=go.Scatter()
    pace_trace=go.Scatter()
    fig = go.Figure(data=None, layout=layout)
    gragh={}
    point_num=2
    app.run_server(debug=True)

