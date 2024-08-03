from nicegui import ui, app, run
from minio import Minio

# Initialize the MinIO client
minio_client = Minio(
    'localhost:9000',
    access_key='minioadmin',
    secret_key='minioadmin',
    secure=False
)



def list_bag_files(bucket_name):
    objects = minio_client.list_objects(bucket_name)
    files = []
    for obj in objects:
        files.append(obj.object_name)
    return files

# select1 = ui.select([1, 2, 3], value=1)


@ui.page("/")
def page():

    current_url = None

    def generate_presigned_url(bucket_name, object_name):
        url = minio_client.presigned_get_object(bucket_name, object_name)
        return url
    
    def display_bag(bag_file):
        nonlocal webviz_iframe
       
        url = generate_presigned_url('ros-data', bag_file)

        #Encode the URL to be able to pass it as a parameter to the iframe
        import urllib.parse

        def encode_url_for_query_parameter(url):
            return urllib.parse.quote(url, safe='')


        full_url = "http://localhost:8081/?remote-bag-url=" + encode_url_for_query_parameter(url)
        webviz_iframe.content = "<iframe src='" + full_url + "' style='width: 150vh; height: 80vh; border: none; '></iframe>"

        current_url = full_url
        print(full_url)
        first = False
        webviz_iframe.visible = True
        
    ui.space()
    ui.label("ROS Bag Visualizer").style("font-size: 48px; font-weight: bold; margin-bottom: 20px;").classes("self-center")

    #Dynamic dropdown menu that will update the list of bag files in the dropdown menu if a new bag file is uploaded to the minio server or if a bag file is deleted from the minio server
    with ui.dropdown_button('Select ROS Bag', auto_close=True).classes("self-center"):
        for bag in list_bag_files('ros-data'):

            ui.item(bag[:-4], on_click=lambda bag=bag: display_bag(bag))


    with ui.row().classes("self-center"):
        webviz_iframe = ui.html('''
                    <iframe src="http://localhost:8081/" style="width: 150vh; height: 80vh; border: none; "></iframe>
    ''')
        
        webviz_iframe.visible = False
    footer = ui.footer(fixed = False).style('').classes("self-center")
    with footer:

        ui.html('''<p>Made with ❤️ by <a href="https://github.com/shubhambhatnag" target="_blank">Shubham</a></p>''').default_style('color: #000000')
ui.run()
