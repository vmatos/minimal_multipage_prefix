from flask import Flask
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash_extensions.enrich import DashProxy, Input, Output
from dash_extensions.enrich import ServersideOutputTransform

from blueprints import page

# Create app.
server = Flask(__name__)
server.url_map.strict_slashes = False
app = DashProxy(
    server=server, 
    suppress_callback_exceptions=False,
    prevent_initial_callbacks=False,
    transforms=[
        ServersideOutputTransform(),
    ],
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP]
)

bp_registry = {}
bp_registry['page1'] = {'bp': page.make_blueprint('page1', 'Page 1 title'), 'label': 'Page 1', 'path': 'page1'}
bp_registry['page2'] = {'bp': page.make_blueprint('page2', 'Page 2 title'), 'label': 'Page 2', 'path': 'page2'}
default_bp = 'page1'

def generate_navbar():
    children = []
    for page in bp_registry.values():
        children.append(dbc.NavLink(children=page['label'], href=page['path'], active="exact", class_name=''))
    navbar = dbc.Nav(
            children=children,
            vertical=True,
            pills=True,
            fill=True,
            class_name='flex-column flex-nowrap overflow-auto p-2'
        )
    return navbar

def generate_layout():
    return html.Div(
        [
            dcc.Location(id='url', refresh=False),
            dbc.Container([
                dbc.Row([
                    dbc.Col(
                        generate_navbar(),
                        width=2, class_name='position-fixed vh-100'),
                    dbc.Col(id='page_content',
                        width=10, class_name='offset-2'),
                ], class_name='bg-light')
            ], fluid=True, class_name='vh-100'),
        ])

@app.callback(
    Output('page_content', 'children'),
    Input('url', 'pathname')
)
def display_widget(pathname):
    bp_name = pathname[1:]
    if bp_name in bp_registry:
        blueprint = bp_registry[bp_name]['bp']
    else:
        blueprint = bp_registry[default_bp]['bp']
    return blueprint.layout()

# Register all blueprint callbacks
for bp in bp_registry.values():
    bp['bp'].register_callbacks(app)

app.layout = generate_layout()
# Prepare the validation layout such that callback registration does not complain
app.validation_layout = html.Div([generate_layout()] + [bp['bp'].layout() for bp in bp_registry.values()])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True,
     dev_tools_hot_reload_max_retry=10,
     dev_tools_silence_routes_logging=False)
