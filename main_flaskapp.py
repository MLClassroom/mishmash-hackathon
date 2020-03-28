from flask import Flask,request, render_template,send_from_directory, session
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from configparser import ConfigParser
from os import environ
from uuid import uuid4
from src.utils.utils import *


#env vars
try :
    conf = ConfigParser()
    conf.read('config.ini')
    blob_conn_string = conf['azblob']['conn_string']
    container_name = conf['azblob']['container_name']

except FileNotFoundError:
    blob_conn_string = environ['blob_conn_string']
    contrainer_name = environ['contrainer_name']


blob_service_client = BlobServiceClient.from_connection_string(blob_conn_string)

app = Flask(__name__,template_folder='templates')

app.secret_key="temp"


@app.route("/",methods=["GET","POST"])
def home():
    return render_template('home.html')

@app.route("/upload",methods=["POST"])
def upload():

    # uploading a file to blob
    print("here")
    try : 
        upload = request.files.getlist("file")[0]
    except IndexError:
        return render_template('home.html')

    temp_path = pjoin("temp",sess_id),
    input_path = pjoin(temp_path,"input")
    output_path = pjoin(temp_path,"output")

    filename = upload.filename
    if filename.endswith("csv") or filename.endswith("xlsx"):
        pass
    else:
        return render_template("error.html", errmsg = "file extension not supported")
    

    local_file_name = pjoin(input_path, filename)
    print(local_file_name)
    upload.save(local_file_name)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)
    with open(local_file_name, "rb") as data:
        blob_client.upload_blob(data)
    print("uploading file to blob done")


    return "upload"


@app.before_request
def before_req():
    session['id']=str(uuid4())
    sess_id = session['id']
    create_folders(sess_id)


# @app.after_request
# def after_req():
#     sess_id = session['id']
#     delete_folders(sess_id)

@app.teardown_request
def teardown_req(error=None):
    sess_id = session['id']
    # delete_folders(sess_id)

if __name__ == "__main__":
    app.run(debug=True, host = "0.0.0.0", port = 8080)