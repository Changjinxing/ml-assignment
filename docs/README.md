
# Running in Your Local Machine

To run the service locally:

1. **Install Required Packages**: Install the required Python packages by running:
    ```bash
    pip install -r requirements.txt
    ```

2. **Run the Service**: Start the service by executing:
    ```bash
    python api.py
    ```

3. **Test the Service**: Open another terminal and test the service by sending a POST request. Use the following command:
    ```bash
    curl --location --request POST 'http://127.0.0.1:9527/translation' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "payload": {
            "fromLang": "en",
            "records": [
                {
                    "id": "123",
                    "text": "Life is like a box of chocolates."
                },
                {
                    "id": "456",
                    "text": "Life is a gift."
                }
            ],
            "toLang": "ja"
        }
    }'
    ```
    You should receive a JSON response with translated text.
    ```json
    {
      "code": 200,
      "result": [
        {
          "id": "123",
          "text": "人生はチョコレートの箱のようなものだ。"
        },
        {
          "id": "456",
          "text": "人生は贈り物です。"
        }
      ],
      "status": "success"
    }
    ```

# Installing Docker on Your System

## For MacBook

1. **Install Docker Desktop**: Download and install Docker Desktop from the official Docker website.

2. **Open Docker Desktop**: After installation, open Docker Desktop application.

3. **Build Your Docker Image**: Navigate to the directory containing your Dockerfile in the terminal and run the following command to build your Docker image:
    ```bash
    docker build -t translation_service_v1 .
    ```

4. **Check the Built Image**: Verify that the image is built successfully by running:
    ```bash
    docker images
    ```
    You should see the image named `translation_service_v1` listed.

5. **Push Image to Docker Hub (Optional)**: If you want to deploy the image to a Kubernetes cluster on the cloud, you may need to push it to Docker Hub. First, log in to Docker Hub using your credentials:
    ```bash
    docker login
    ```
    Then tag your image and push it to Docker Hub:
    ```bash
    docker tag translation_service_v1:latest yourusername/translation_service_v1:latest
    docker push yourusername/translation_service_v1:latest
    ```

6. **Deploy Image to a Container**: Use `kubectl` to deploy the image to a container on your local machine:
    ```bash
    kubectl apply -f deployment.yaml
    ```
    Ensure Docker Desktop Kubernetes Cluster is started before this step.

    - **Start Docker Desktop Kubernetes Cluster**: 
        1. Open the Docker Desktop application.
        2. Go to Docker Desktop preferences by clicking on Docker Desktop in the top menu bar and selecting "Preferences".
        3. In the Preferences window, navigate to the Kubernetes tab.
        4. Check the box to enable Kubernetes and save the changes.
        5. Docker Desktop will start the local Kubernetes cluster.

    After starting the Docker Desktop Kubernetes cluster, you will see the information like below:
    ```bash
    deployment.apps/translation-service created
    ```

7. **Check Pod Status**: Confirm that the pod is running by executing:
    ```bash
    kubectl get deployments
    kubectl get pods
    ```
    If successful, you should see the pod is running like below:
    ```bash
    NAME                                   READY   STATUS    RESTARTS   AGE
    translation-service-769878f4bd-z5g76   1/1     Running   0          7s
    ```

8. **Check Service Status**: Verify that the service is running with:
    ```bash
    kubectl get services
    ```
    If successful, you should see the service is running like below:
    ```bash
    NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
    kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   25m
    ```

