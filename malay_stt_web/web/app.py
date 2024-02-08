import os
from flask import Flask, flash, request, redirect, url_for
from secrets import token_urlsafe
from markupsafe import escape
from werkzeug.utils import secure_filename
from html_template import default_html
from malay_stt_web.speech.speech import speech_to_text
from utils import allowed_file

UPLOAD_FOLDER = "/home/mirul/workspace/malay_tts_web/uploads"


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            # flash("No file part")
            return """
                    <form method=post enctype=multipart/form-data hx-post="/">
                        <p>No file part</p>
                        <input type=file name=file>
                        <input type=submit value=Upload>
                    </form>
                    """
        file = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            # flash("No selected file")
            return """
                    <form method=post enctype=multipart/form-data hx-post="/">
                        <p>No selected file</p>
                        <input type=file name=file>
                        <input type=submit value=Upload>
                    </form>
                    """
        if file and allowed_file(file.filename):
            filename = secure_filename(f"{token_urlsafe(6)}-{file.filename}")
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return f"""
                    <form method=post enctype=multipart/form-data hx-post="/">
                        <p>Success! the filename is {filename}</p>
                        <input type=file name=file>
                        <input type=submit value=Upload>
                    </form>
                    """

    return default_html(
        "Upload File",
        """
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data hx-post="/">
        <input type=file name=file>
        <input type=submit value=Upload>
    </form>""",
    )


@app.route("/stt/<file_name>", methods=["GET"])
def stt(file_name):
    path = os.path.join(app.config["UPLOAD_FOLDER"], escape(file_name))
    res = speech_to_text(path)
    return default_html(
        f"Result for {file_name}",
        f"""
    <h1>Result for {file_name}</h1>
    <code>{res}</code>
    """,
    )


@app.route("/about")
def about():
    return default_html("Index", "About page")
