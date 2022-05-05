from flask import Flask, request

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    html = f"""
            <H3>Dashboard not found.</H3>
            <p>Trying to [{request.method}] path: "/{path}"</p>
            """
    return html