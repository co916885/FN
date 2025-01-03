from flask import Flask, render_template, request, jsonify
import os
import time
import pathlib
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)

# 加載環境變量
env_path = pathlib.Path(".env")
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

azure_connection_string = os.getenv("azure_connection_string")
container_name = os.getenv("container_name")

blob_service_client = BlobServiceClient.from_connection_string(azure_connection_string)
container_client = blob_service_client.get_container_client(container_name)

# 上傳圖片到 Azure
def upload_to_azure(file):
    try:
        # 使用時間戳生成唯一的圖片檔名
        photo_name = f"photo_{time.strftime('%Y%m%d_%H%M%S')}.jpg"
        blob_client = container_client.get_blob_client(photo_name)

        # 上傳圖片檔案
        blob_client.upload_blob(file, overwrite=True)
        return f"文件 {photo_name} 已上傳至 Azure Blob"
    except Exception as e:
        return f"上傳失敗: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # 如果是上傳圖片
        if 'file' in request.files:
            file = request.files['file']
            # 如果有檔案，則將其上傳至 Azure Blob
            message = upload_to_azure(file)
            return render_template("index.html", success_message=message)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
