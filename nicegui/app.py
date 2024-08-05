from nicegui import ui, app, run
from minio import Minio
import urllib.parse
import os

# Initialize the MinIO client
minio_client = Minio(
    'minio:9000',
    access_key='minioadmin',
    secret_key='minioadmin',
    secure=False
)
WEBVIZ_URL = os.getenv('WEBVIZ_URL', 'http://localhost/webviz')

# Function to modify the presigned URL
def modify_presigned_url(presigned_url):
    base_url = 'http://localhost/minio'
    modified_url = presigned_url.replace('http://minio:9000', base_url)
    return modified_url

# Function to generate a presigned URL for the specified object in the specified bucket
def generate_presigned_url(bucket_name, object_name):
    url = minio_client.presigned_get_object(bucket_name, object_name)
    return modify_presigned_url(url)

# Returns a list of all the bag files in the specified bucket
def list_bag_files(bucket_name):
    objects = minio_client.list_objects(bucket_name)
    files = []
    for obj in objects:
        files.append(obj.object_name)
    return files

@ui.page("/")
def page():
    test_url = "http://localhost/webviz/?remote-bag-url=http%3A%2F%2Flocalhost%2Fminio%2Fros-data%2Frecorded_data_11_01_56.bag%3FX-Amz-Algorithm%3DAWS4-HMAC-SHA256%26X-Amz-Credential%3Dminioadmin%252F20240804%252Fus-east-1%252Fs3%252Faws4_request%26X-Amz-Date%3D20240804T193815Z%26X-Amz-Expires%3D604800%26X-Amz-SignedHeaders%3Dhost%26X-Amz-Signature%3D3c4bb5ea0da319edd2e0f67828a039a0293fe75748b41f71c012fb837e1d22e7&seek-to=1694185322.908547472&layout_url=https%3A%2F%2Fapi.npoint.io%2Fd8cdfcecc99b68123ac7"
    # test = ui.html(f"""
    # <iframe src="{test_url}" style="width: 150vh; height: 80vh; border: none;">
    #     <base href="http://localhost/webviz/">
    # </iframe>
    # """)

    def apply_layout(index):
        nonlocal webviz_iframe
        nonlocal current_url

        layouts = [
            "https%3A%2F%2Fapi.npoint.io%2F6b92217796bcefd2ac95",
            "https%3A%2F%2Fapi.npoint.io%2Fd8cdfcecc99b68123ac7",
            "https%3A%2F%2Fapi.npoint.io%2F71106a2b8f068b8b6975"
        ]

        new_url = current_url + "&layout-url=" + layouts[index - 1]
        webviz_iframe.content = f"""
        <iframe src="{new_url}" style="width: 150vh; height: 80vh; border: none;">
            <base href="http://localhost/webviz/">
        </iframe>
        """

    current_url = None

    def display_bag(bag_file):
        nonlocal layouts
        nonlocal webviz_iframe
        nonlocal current_url
        nonlocal selected
        nonlocal layout_toggle
        print("Attempting to display bag: ", bag_file, flush=True)
        url = generate_presigned_url('ros-data', bag_file)
        full_url = f"{WEBVIZ_URL}/?remote-bag-url={urllib.parse.quote(url, safe='')}"
        full_url_with_layout = full_url + "&layout-url=https%3A%2F%2Fapi.npoint.io%2F6b92217796bcefd2ac95"

        webviz_iframe.content = f"""
        <iframe src="{full_url_with_layout}" style="width: 150vh; height: 80vh; border: none; overflow: hidden;">
            <base href="http://localhost/webviz/">
        </iframe>
        """
        current_url = full_url

        layouts.visible = True
        layout_toggle.value = 1
        webviz_iframe.visible = True
        selected.text = "Selected ROS Bag: " + bag_file[:-4] + ".bag"

    ui.space()
    ui.label("ROS Bag Visualizer").style("font-size: 48px; font-weight: bold;").classes("self-center")
    selected = ui.label("Selected ROS Bag: None").style("font-size: 24px;").classes("self-center")

    with ui.dropdown_button('Select ROS Bag', auto_close=True).classes("self-center"):
        for bag in list_bag_files('ros-data'):
            ui.item(bag[:-4], on_click=lambda bag=bag: display_bag(bag))

    layouts = ui.row().classes("self-center")
    with layouts:
        ui.label("Select Layout: ").style("font-size: 24px;")
        layout_toggle = ui.toggle([1, 2, 3], value=1, on_change=lambda toggle: apply_layout(toggle.value))

    layouts.visible = False

    with ui.row().classes("self-center"):
        webviz_iframe = ui.html('')
        webviz_iframe.visible = False
    
    footer = ui.footer(fixed=False).style('').classes("self-center")

    with footer:
        ui.html('''
            <style>
            p {
                color: white;
            }
            </style>
            <p>Made with ❤️ by <u><a href="https://github.com/shubhambhatnag" target="_blank">Shubham</a></u></p>
        ''').default_style('color: #000000')

print("Running the app")
ui.run()
