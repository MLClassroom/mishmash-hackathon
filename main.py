import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

# Bootstrap for layout.
app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501

# styles
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}
markdown_text = '''
# MishMash Hackathon
### Team_gep 
Nishanth,Hillol,Harsha,Ginni
'''



app.layout = html.Div([
    html.Div([
            dcc.Markdown(children=markdown_text)
        ], 
        style={'textAlign':'center'}
            ),
    html.Div([
            dcc.Location(id='url', refresh=False),
            html.Div(id='page-content')
        ]
    )
])

upload = html.Div([dcc.Upload([
        'Drag and Drop or ',
        html.A('Select a File')
    ], style={
        'width': '100%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center'
    })
])

index_page = html.Div([app.layout,
    dcc.Link('Go to upload', href='/upload'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
])

upload_layout = html.Div([app.layout,upload,
    dcc.Link('Go to upload', href='/upload'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
])





# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/upload':
        return upload_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return index_page

if __name__ == '__main__':
    app.run_server(debug=True,port=8080)