from flask import Flask, jsonify, request
from minio import Minio

app = Flask(__name__)

# Initialize the MinIO client
minio_client = Minio(
    'localhost:9000',
    access_key='minioadmin',
    secret_key='minioadmin',
    secure=False
)

@app.route('/api/bagfiles', methods=['GET'])
def list_bag_files():
    bucket_name = 'rosbags'
    objects = minio_client.list_objects(bucket_name)
    files = []
    for obj in objects:
        files.append(obj.object_name)
    return jsonify(files)

@app.route('/api/presigned-url', methods=['GET'])
def get_presigned_url():
    bucket_name = 'ros-data'
    object_name = request.args.get('file')
    url = minio_client.presigned_get_object(bucket_name, object_name)
    return jsonify({'url': url})

if __name__ == '__main__':
    app.run(port=5000)
