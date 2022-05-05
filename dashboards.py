from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from app_default_landing.app import app as default_app
from app1.app import server as app1_server
from app2.app import server as app2_server

multiple_apps = DispatcherMiddleware(default_app,
    {
        '/app1': app1_server,
        '/app2': app2_server,
    }
)

if __name__ == '__main__':
    run_simple(
        hostname='localhost',
        port=8080,
        application=multiple_apps,
        use_reloader=True,
        use_debugger=True,
        use_evalex=True
    )
