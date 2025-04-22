# Training Environment Setup

This repository contains a Dockerized training environment including Jupyter Lab and supporting services.

## Prerequisites

* [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* [Docker](https://docs.docker.com/get-docker/)

## Setup and Deployment

1.  **Clone the Repository:**
    ```bash
    git clone <your-repo-url>
    cd your-training-repo
    ```

2.  **Deploy the Environment:**
    Run the deployment script. This will build the necessary Docker images (can take a while the first time) and start all the containers in the background.
    ```bash
    ./deploy.sh
    ```

## Accessing the Environment

1.  **Jupyter Lab:**
    Open your web browser and navigate to [http://localhost:8888](http://localhost:8888).
