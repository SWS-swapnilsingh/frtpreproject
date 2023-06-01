from flask import Flask, render_template, request, redirect
import os
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)

connect_str = "DefaultEndpointsProtocol=https;AccountName=mystorageaccountname007;AccountKey=oAzzwxIaybYW6Qk0/T7SgWRXOsAJ2LHS6ftxEBTsjeNQ5AF5DavNI7zx3dJ8IaZoysfOSsGT7r1++AStj+ucvg==;EndpointSuffix=core.windows.net"
container_name = "photos"
blob_service_client = BlobServiceClient.from_connection_string(conn_str=connect_str)
try:
    container_client = blob_service_client.get_container_client(container=container_name)
    container_client.get_container_properties()
except Exception as e:
    container_client = blob_service_client.create_container(container_name)


@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/photos', methods=['GET','POST'])
def myphotos():
    blob_items = container_client.list_blobs()
    
    # img_html = ""
    list_urls = []

    for blob in blob_items:
        blob_client = container_client.get_blob_client(blob=blob.name)
        # img_html += "<img src='{}' width='auto' height='200' />".format(blob_client.url)
        list_urls.append(blob_client.url)
    print(list_urls)
    return render_template('photos.html', list_urls = list_urls)


    # blob_items = container_client.list_blobs()


    # img_html = ""
    

    # for blob in blob_items:
    #     blob_client = container_client.get_blob_client(blob=blob.name)
    #     img_html += "<img src='{}' width='auto' height='200' />".format(blob_client.url)
    # print(img_html)
    # return '''
    # <h1>Photos of School and children</h1>
    # <form method = "post" action = "/upload-photos" enctype = "multipart/form-data">
    # <input type="file" name="photos" multiple >
    # <input type="submit">
    # </form>
    # '''+ img_html


@app.route("/upload-photos", methods=['POST'])
def upload_photos():
    filenames = ""
    for file in request.files.getlist("photos"):
        try:
            container_client.upload_blob(file.filename, file)
            filenames += file.filename + "<br />"
        except Exception as e:
            print(e)
            print("Ignoring duplicate filenames")
    # return "<p>Uploaded: <br />{}</p>".format(filenames)
    return redirect('/photos')

if __name__=="__main__":
    app.run(debug=True)