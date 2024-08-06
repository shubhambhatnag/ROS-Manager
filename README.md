

# ROS Manager

ROS Manager integrates NiceGUI, MinIO, and Webviz using Docker and NGINX. The goal is to provide a seamless interface for visualizing ROS bag files stored in MinIO and viewed through Webviz.

![Example gif](https://i.imgur.com/WcQcQzB.gif)

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Deployment](#deployment)
- [Usage](#usage)

## Prerequisites

Before you begin, ensure you have the following installed:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Git](https://git-scm.com/)
- [Python (Newest stable 3.X reccomended) ](https://www.python.org/downloads/)

## Setup

1. **Clone the Repository**

  
   ```git clone https://github.com/shubhambhatnag/ROS-Manager.git``` \
   ```cd ROS-Manager```

## Deployment

1. **Build and Start the Docker Containers**

   Navigate to the root directory of the project and run (Make sure docker is running):

   


   ```docker-compose up --build -d```



   This command will build the Docker images and start the containers for MinIO, Webviz, NiceGUI, and NGINX.

2. **Access the Application**

   Once the containers are running, access the application via:

   

    ```http://localhost``` (Google Chrome strongly recommended)



   - MinIO Console: ```http://localhost/minio-console```
   - Webviz: ```http://localhost/webviz```
   - NiceGUI Interface: ```http://localhost```

## Usage

1. **Uploading ROS Bag Files to MinIO**

   - Access the MinIO console by pressing the button on the app, or open ```http://localhost/minio-console```
   - Login with username and password (both are "minioadmin")
   - Use the MinIO console to upload ROS bag files to the ros-data bucket (Bucket should already be created for you, but in the event that it does not exist please create a new bucket titled 'ros-data').

2. **Visualizing ROS Bag Files**

   - Access the NiceGUI interface at ```http://localhost```
   - Select a ROS bag file from the dropdown menu to visualize it using Webviz.
   - If new bags are added to bucket, please reload the page.

3. **Editing Layout**

   - Use the toggle to select which pre-determined layout to use
   - The Webviz app also allows you to set your own layout, and import/export your own JSON layouts (top right)

4. **Closing Application**

   - To close the application and spin down all services , run ```docker compose down```






