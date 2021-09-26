#Main python code (to hold API)

from flask import Flask, request, render_template, send_file

from API import API as api

INPUT_FILE = "Senbonzakura.mxl"
OUTPUT_FILE = "output.mxl"

app = Flask(__name__,
    static_url_path="",
    static_folder = "web/static",
    template_folder="web/templates"
)
app.config["DEBUG"] = True

#Static Routes
@app.route("/")
def default():
    return render_template("index.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/viewer")
def viewer():
    return render_template("viewer.html")

import pdb

#Call API
import base64
@app.route('/api/annotate', methods=['POST'])
def home():
    uploaded_file = request.files['input_file']
    filename = base64.b64encode(uploaded_file.filename.encode('ascii'))
    uploaded_file.save(f"input/{filename}.mxl")
    api.process_file(f"input/{filename}.mxl", f"output/{filename}")
    return filename

#Get File
@app.route("/notes/<note_id>")
def get_notes(note_id):
    return open(f"output/{note_id}", "rb").read()

app.run()
print("Server Launched")