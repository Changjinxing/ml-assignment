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

5. **Deploy Image to a Container**: Use `kubectl` to deploy the image to a container on your local machine:
    ```bash
    kubectl apply -f deployment.yaml
    ```
    Ensure Docker Desktop Kubernetes Cluster is started before this step.

6. **Check Pod Status**: Confirm that the pod is running by executing:
    ```bash
    kubectl get deployments
    kubectl get pods
    ```

7. **Check Service Status**: Verify that the service is running with:
    ```bash
    kubectl get services
    ```

# Running in Your Local Machine

1. **Install Required Packages**: Install the required Python packages by running:
    ```bash
    pip install -r requirements.txt
    ```

2. **Run the Service**: Start the service by executing:
    ```bash
    python api.py
    ```

3. **Test the Service**: Open another terminal and test the service by sending a POST request:
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

