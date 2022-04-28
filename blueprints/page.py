from dash_extensions.enrich import DashBlueprint, PrefixIdTransform
from dash_extensions.enrich import Input, Output, State, ServersideOutput
from dash import html, dcc
from dash import callback_context, no_update
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

def make_blueprint(prefix, title):
    blueprint = DashBlueprint(transforms=[PrefixIdTransform(prefix=prefix)])

    """
    The dash layout, which uses the callback functions to draw empty graphs
    """
    def generate_layout():
        layout = dbc.Container(children=[], class_name='bg-white rounded mt-2 mb-2')
        layout.children += [dbc.Row(dbc.Col(html.H1(title)))]
        layout.children += [dbc.Row(
            dcc.Loading(
                [
                    dcc.Store(id='graph-data'),
                    dbc.Col(dbc.Button(id='button', children='Graph'))
                ]
            )
        )]
        layout.children += [dbc.Row(
            dbc.Col(dcc.Graph(id='graph'))
        )]
        return layout

    @blueprint.callback(
        ServersideOutput('graph-data', 'data'),
        Input('button', 'n_clicks')
    )
    def load_data(n_clicks):
        time.sleep(2)
        return pd.DataFrame({
            "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
            "Amount": [4, 1, 2, 2, 4, 5],
            "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
        })

    @blueprint.callback(
        Output('graph', 'figure'),
        Input('graph-data', 'data')
    )
    def update_graph(df):
        return px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
    
    blueprint.layout = generate_layout

    return blueprint
