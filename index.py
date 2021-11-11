import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly as go
import pandas as pd
import datetime as datetime

day = datetime.datetime.today().weekday()+1 # saves current day (monday=0 & sunday=6)+1

# Read in csv files
ssh_data = pd.read_csv("/Users/admin/git/MSc_Project/SD_Project/csv/Day4/sshD4.csv")
telnet_data = pd.read_csv("/Users/admin/git/MSc_Project/SD_Project/csv/Day4/telnetD4.csv")
http_data = pd.read_csv("/Users/admin/git/MSc_Project/SD_Project/csv/Day4/httpD4.csv")
https_data = pd.read_csv("/Users/admin/git/MSc_Project/SD_Project/csv/Day4/httpsD4.csv")


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
            html.H6('Dashboard last updated: ' + str(datetime.datetime.strptime(ssh_data['timestamp'].iloc[-1], '%Y-%m-%d %H:%M:%S.%f').strftime("%B %d, %Y at %H:%M (BST)")),
                    style={'color': 'orange'})

        ], className='one-third column', id = 'title1')

    ], id = 'header', className = 'row flex-display', style={'margin-bottom': '25px'}),

# Second row
    html.Div([
        html.Div([
            html.H5('Non-control Honeypot', style={'margin-bottom': '0px', 'color': 'blue'})
        ])
    ], className='one-third column'),

# Third row of the dashboard app
    #Third row first column
    html.Div([
        html.Div([
            html.H6(children='Total SSH connections:',
                    style={'textAlign': 'center',
                    'color': 'white'}),
            html.P(f"{ssh_data.shape[0]: .0f}",  #paragraph
                   style={'textAlign': 'center',
                    'color': 'orange',
                          'fontSize': 30}
                   )

        ], className='card_container three columns'),

#Third row second column
html.Div([
            html.H6(children='Total Telnet connections:',
                    style={'textAlign': 'center',
                    'color': 'white'}),
            html.P(f"{'X'}", #paragraph
                   style={'textAlign': 'center',
                    'color': '#dd1e35',
                          'fontSize': 30}
                   )

        ], className='card_container three columns'),

#Third row third column
html.Div([
            html.H6(children='Total HTTP connections:',
                    style={'textAlign': 'center',
                    'color': 'white'}),
            html.P(f"{'X'}", #paragraph
                   style={'textAlign': 'center',
                    'color': 'yellow',
                          'fontSize': 30}
                   )

        ], className='card_container three columns'),

#Third row fourth column
html.Div([
            html.H6(children='Total HTTPS connections:',
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

# Fourth row of the dashboard app
html.Div([
        html.Div([
            html.H5('Control Honeypot', style={'margin-bottom': '0px', 'color': 'blue'})
        ])
    ], className='one-third column'),

# Fifth row of the dashboard app
    #Second row first column
    html.Div([
        html.Div([
            html.H6(children='Total SSH connections:',
                    style={'textAlign': 'center',
                    'color': 'white'}),
            html.P(f"{ssh_data.shape[0]: .0f}",  #paragraph
                   style={'textAlign': 'center',
                    'color': 'orange',
                          'fontSize': 30}
                   )

        ], className='card_container three columns'),

#Fifth row second column
html.Div([
            html.H6(children='Total Telnet connections:',
                    style={'textAlign': 'center',
                    'color': 'white'}),
            html.P(f"{'X'}", #paragraph
                   style={'textAlign': 'center',
                    'color': '#dd1e35',
                          'fontSize': 30}
                   )

        ], className='card_container three columns'),

#Fifth row third column
html.Div([
            html.H6(children='Total HTTP connections:',
                    style={'textAlign': 'center',
                    'color': 'white'}),
            html.P(f"{'X'}", #paragraph
                   style={'textAlign': 'center',
                    'color': 'yellow',
                          'fontSize': 30}
                   )

        ], className='card_container three columns'),

#Fifth row fourth column
html.Div([
            html.H6(children='Total HTTPS connections:',
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

#Sixth row
    html.Div([
        html.Div([
            html.P('Select honeypot:', className='fix_label', style={'color':'white'}),
            dcc.Dropdown(id = 'ip',
                         multi =  False,
                         searchable=True,
                         value='',
                         placeholder='SSH/Telnet/Http',
                         options=[{'label':c,'value':c}
                                  for c in (ssh_data['ip'].unique())], className='dcc_compon'),
            dcc.Graph(id='confirmed', config={'displayModeBar': False}, className='dcc_compon')


        ],className='create_container three columns')
    ],className='row flex-display'),

], id = 'mainContainer', style={'display': 'flex', 'flex-direction': 'column'})

#@app.callback(Output('confirmed','figure'),#
#              [Input('w_countires','value')])
#def update_confirmed(w_countries):


if __name__ == '__main__':
    app.run_server(debug=True)










