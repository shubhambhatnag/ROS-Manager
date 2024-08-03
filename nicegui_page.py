from nicegui import ui, app, run
from minio import Minio
import urllib.parse

# Initialize the MinIO client
minio_client = Minio(
    'localhost:9000',
    access_key='minioadmin',
    secret_key='minioadmin',
    secure=False
)


#Returns a list of all the bag files in the specified bucket
def list_bag_files(bucket_name):
    objects = minio_client.list_objects(bucket_name)
    files = []
    for obj in objects:
        files.append(obj.object_name)
    return files


#This decorator allows for a unique page for each user - without it, every user would see the same page and would be affected by each other's actions
@ui.page("/")
def page():


    def apply_layout(index):
        nonlocal webviz_iframe
        nonlocal current_url

        #Applies layout to the webviz visualizer based on the index of the layout button clicked
        #This approach allows for easy addition of more layouts in the future

        #Layouts hostied on npoint.io (Free JSON hosting service)
        layouts = ["https%3A%2F%2Fapi.npoint.io%2F6b92217796bcefd2ac95","https%3A%2F%2Fapi.npoint.io%2Fd8cdfcecc99b68123ac7","https%3A%2F%2Fapi.npoint.io%2F71106a2b8f068b8b6975"]
        
        new_url = current_url + "&layout-url=" + layouts[index - 1]
        webviz_iframe.content = "<iframe src='" + new_url + "' style='width: 150vh; height: 80vh; border: none; '></iframe>"

    #Tracks the current URL being displayed in the iframe; Allows for easy switching between layouts as shown in the apply_layout function
    current_url = None

    #Generates a presigned URL for the specified object in the specified bucket
    def generate_presigned_url(bucket_name, object_name):
        url = minio_client.presigned_get_object(bucket_name, object_name)
        return url

    #Generates the URL for the webviz visualizer and displays it in the iframe    
    def display_bag(bag_file):
        nonlocal layouts
        nonlocal webviz_iframe
        nonlocal current_url
        nonlocal selected

        #Uses minio to generate a presigned URL for the bag file
        url = generate_presigned_url('ros-data', bag_file)

        
        
        #Encode the URL to be able to pass it as a parameter to the iframe
        def encode_url_for_query_parameter(url):
            return urllib.parse.quote(url, safe='')

        #Generate the full URL for the webviz visualizer 
        full_url = "http://localhost:8081/?remote-bag-url=" + encode_url_for_query_parameter(url)

        #Add the default layout URL (just in case) to the full URL

        full_url_with_layout = full_url + "&layout-url=https%3A%2F%2Fapi.npoint.io%2F6b92217796bcefd2ac95"

        #Generate the iframe with the URL with HTML styling
        webviz_iframe.content = "<iframe src='" + full_url_with_layout + "' style='width: 150vh; height: 80vh; border: none; overflow: hidden; '></iframe>"

        #Update the current URL
        current_url = full_url
        
        #Make the layout buttons and the iframe visible
        layouts.visible = True
        webviz_iframe.visible = True

        #Update the selected bag label
        selected.text = "Selected ROS Bag: " + bag_file[:-4] + ".bag"
        

    ui.space()

    ui.label("ROS Bag Visualizer").style("font-size: 48px; font-weight: bold;").classes("self-center")


    selected = ui.label("Selected ROS Bag: None").style("font-size: 24px;").classes("self-center")
    #Dynamic dropdown menu that will update the list of bag files in the dropdown menu if a new bag file is uploaded to the minio server or if a bag file is deleted from the minio server
    with ui.dropdown_button('Select ROS Bag', auto_close=True).classes("self-center"):
        for bag in list_bag_files('ros-data'):

            ui.item(bag[:-4], on_click=lambda bag=bag: display_bag(bag))



    #Layout toggle - initially hidden since the webviz visualizer is also hidden
    layouts = ui.row().classes("self-center")
    with layouts:
        ui.label("Select Layout: ").style("font-size: 24px;")
        layout_toggle = ui.toggle([1, 2, 3], value=1, on_change=lambda toggle: apply_layout(toggle.value))


    layouts.visible = False




    #Injected iframe to display the webviz visualizer - initially hidden
    with ui.row().classes("self-center"):
        webviz_iframe = ui.html('''
                    <iframe src="http://localhost:8081/" style="width: 150vh; height: 80vh; border: none; "></iframe>
    ''')
        
        webviz_iframe.visible = False



    #Injected HTML to create the footer
    footer = ui.footer(fixed = False).style('').classes("self-center")
    with footer:
        
        ui.html('''
                <style>
                p {
                    color: white;
                }
                </style>
                
                <p>Made with ❤️ by <u><a href="https://github.com/shubhambhatnag" target="_blank">Shubham</a></u></p>                   
            ''').default_style('color: #000000')
        


#Runs the app
ui.run()
