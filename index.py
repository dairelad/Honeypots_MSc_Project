import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

ssh_log = pd.read_csv("ssh_log.csv")

app = dash.Dash(__name__, )

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('UofG_logo.png'),
                     id = 'corona-image',
                     style={'height': '100px',
                            'width': 'auto',
                            'margin-bottom': '25px'})

        ], className='one-third column'),

        html.Div([
            html.Div([
                html.H3('UofG MSc IT+ Honeypot Project Dashboard', style={'margin-bottom': '0px', 'color': 'white'}),
                html.H5('GUID: 2591168o', style={'margin-bottom': '0px', 'color': 'white'})
            ])
        ], className='one-half column', id = 'title'),

        html.Div([
            html.H6('Total number of SSH connections: ',
                    style={'color': 'orange'})

        ], className='one-third column', id = 'title1')

    ], id = 'header', className = 'row flex-display', style={'margin-bottom': '25px'})
], id = 'mainContainer', style={'display': 'flex', 'flex-direction': 'column'})

if __name__ == '__main__':
    app.run_server(debug=True)










