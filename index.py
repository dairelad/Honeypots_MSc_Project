import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly as go
import pandas as pd
import datetime as datetime

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
            html.H6('Dashboard last updated: ' + str(datetime.datetime.strptime(ssh_log['timestamp'].iloc[-1], '%Y-%m-%d %H:%M:%S.%f').strftime("%B %d, %Y at %H:%M (BST)")),
                    style={'color': 'orange'})

        ], className='one-third column', id = 'title1')

    ], id = 'header', className = 'row flex-display', style={'margin-bottom': '25px'}),

# Second row of the dashboard app
    #Second row first column
    html.Div([
        html.Div([
            html.H6(children='Honeypot 1 - Total SSH connections:',
                    style={'textAlign': 'center',
                    'color': 'white'}),
            html.P(f"{ssh_log.shape[0]: .0f}", #paragraph
                   style={'textAlign': 'center',
                    'color': 'orange',
                          'fontSize': 30}
                   )

        ], className='card_container three columns'),

#Second row second column
html.Div([
            html.H6(children='Honeypot 1 - Total Telnet connections:',
                    style={'textAlign': 'center',
                    'color': 'white'}),
            html.P(f"{'X'}", #paragraph
                   style={'textAlign': 'center',
                    'color': '#dd1e35',
                          'fontSize': 30}
                   )

        ], className='card_container three columns'),

#Second row third column
html.Div([
            html.H6(children='Honeypot 2 - Total SSH connections:',
                    style={'textAlign': 'center',
                    'color': 'white'}),
            html.P(f"{'X'}", #paragraph
                   style={'textAlign': 'center',
                    'color': 'yellow',
                          'fontSize': 30}
                   )

        ], className='card_container three columns'),

#Second row fourth column
html.Div([
            html.H6(children='Honeypot 2 - Total SSH connections:',
                    style={'textAlign': 'center',
                    'color': 'white'}),
            html.P(f"{'X'}", #paragraph
                   style={'textAlign': 'center',
                    'color': '#66ff66',
                          'fontSize': 30}
                   )
        ],
    className='card_container three columns')

    ], className='row flex display'),

    html.Div([
        html.Div([
            html.P('Select honeypot:', className='fix_label', style={'color':'white'}),
            dcc.Dropdown(id = 'ip',
                         multi =  False,
                         searchable=True,
                         value='',
                         placeholder='SSH/Telnet/Http',
                         options=[{'label':c,'value':c}
                         for c in (ssh_log['ip'].unique())], className='dcc_compon'),
            dcc.Graph(id='confirmed', config={'displayModeBar': False}, className='dcc_compon')


        ],className='create_container three columns')
    ],className='row flex-display'),

], id = 'mainContainer', style={'display': 'flex', 'flex-direction': 'column'})

#@app.callback(Output('confirmed','figure'),#
#              [Input('w_countires','value')])
#def update_confirmed(w_countries):


if __name__ == '__main__':
    app.run_server(debug=True)










