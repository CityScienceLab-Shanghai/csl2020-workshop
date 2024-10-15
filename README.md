
# CityScienceSummit 2020 Workshop - Equity Without Zoning

## Introduction

Welcome to the **CityScienceSummit 2020 Workshop - Equity Without Zoning**. This workshop explores innovative ways to promote urban equity without relying on traditional zoning practices. For a brief introduction, watch the video below:

[![Watch the Introduction Video](https://img.youtube.com/vi/-oN33g7ALaw/0.jpg)](https://www.youtube.com/watch?v=-oN33g7ALaw)

Click the image above to watch the introduction video on YouTube.

---

## Demo and Deployment

This repository contains the materials and resources for the CityScienceSummit 2020 Workshop on "Equity Without Zoning." The workshop content can be easily deployed locally using Docker. Below are the steps to set up and run the demo.

### Prerequisites

Ensure Docker is installed on your machine. If you do not have Docker installed, you can download it from [here](https://www.docker.com/get-started).

### Deployment Steps

1. **Pull the Docker image:**

   Open a terminal and run the following command to pull the Docker image:

   ```bash
   docker pull jajamoa/css2020:v1
   ```

2. **Run the Docker container:**

   After pulling the image, start the container by running the following command:

   ```bash
   sudo docker run -d -p 1239:80 --name CSS jajamoa/css2020:latest sh entry.sh
   ```

3. **Access the workshop content:**

   Once the container is running, visit `http://localhost:1239` in your browser to access the workshop materials locally.

---

For more information about the Docker image, visit our [Docker Hub page](https://hub.docker.com/r/jajamoa/css2020).
