

# ROS Visualizer

ROS Visualizer integrates NiceGUI, MinIO, and Webviz using Docker and NGINX. The goal is to provide a seamless interface for visualizing ROS bag files stored in MinIO and viewed through Webviz.

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

## Setup

1. **Clone the Repository**

  
   git clone https://github.com/shubhambhatnag/ROS-Manager.git \
   cd nicegui-minio-webviz


## Deployment

1. **Build and Start the Docker Containers**

   Navigate to the root directory of the project and run:

   


   docker-compose up --build -d



   This command will build the Docker images and start the containers for MinIO, Webviz, NiceGUI, and NGINX.

2. **Access the Application**

   Once the containers are running, access the application via:

   

    http://localhost



   - MinIO Console: http://localhost/minio-console
   - Webviz: http://localhost/webviz
   - NiceGUI Interface: http://localhost

## Usage

1. **Uploading ROS Bag Files to MinIO**

   - Access the MinIO console at http://localhost/minio-console
   - Use the MinIO console to upload ROS bag files to the ros-data bucket.

2. **Visualizing ROS Bag Files**

   - Access the NiceGUI interface at http://localhost
   - Select a ROS bag file from the dropdown menu to visualize it using Webviz.

2. **Editing Layout**

   - Use the toggle to select which pre-determined layout to use
   - The webviz app also allows you to set your own layout, and import JSON layouts (top right)




