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
ui.space()
ui.label("ROS Bag Visualizer").style("font-size: 48px; font-weight: bold; margin-bottom: 20px;").classes("self-center")

#Dynamic dropdown menu that will update the list of bag files in the dropdown menu if a new bag file is uploaded to the minio server or if a bag file is deleted from the minio server
with ui.dropdown_button('Select ROS Bag', auto_close=True).classes("self-center"):
    for bag in list_bag_files('ros-data'):

        ui.item(bag[:-4], on_click=lambda bag=bag: ui.notify("Selected: " + bag)).classes("self-center")

footer = ui.footer(fixed = False).style('').classes("self-center")
with footer:

    ui.html('''<p>Made with ❤️ by <a href="https://github.com/shubhambhatnag" target="_blank">Shubham</a></p>''').default_style('color: #000000')
ui.run()
