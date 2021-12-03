from flask import Flask, request, send_file
import microservice as sv

app = Flask(__name__)

@app.route('/', methods=['POST']) 
def foo():
    data = request.json

    for key in data:
        sv.variables[key] = data[key]
    
    try:
        return send_file(sv.drawGraph(), attachment_filename=f"{sv.variables['filename']}.{sv.variables['output']}")
    except Exception as e:
        return str(e)