# install docker on your system
## macbook
1. install docker desktop 

2. open docker desktop

3. build your docker image(need to be in the directory that contains the Dockerfile)
```bash
docker build -t translation_service_v1 .
```

4. check the image is built successfully
```bash
docker images
```
You should see the image name `translation_service_v1` like below
```bash
REPOSITORY               TAG       IMAGE ID       CREATED          SIZE
translation_service_v1   latest    0840dd7b3a7a   52 seconds ago   742MB
```
You may need to push your image to docker hub if you want to deploy it to kubernetes cluster on cloud
```bash
docker login
docker tag translation_service_v1:latest yourusername/translation_service_v1:latest
docker push yourusername/translation_service_v1:latest
````

5. deploy the image to a container on your local machine
```bash
kubectl apply -f deployment.yaml
```
For macbook, you may also need to Start Docker Desktop Kubernetes Cluster first
1. Open the Docker Desktop application.
2. Go to Docker Desktop preferences by clicking on Docker Desktop in the top menu bar and selecting "Preferences".
3. In the Preferences window, navigate to the Kubernetes tab.
4. Check the box to enable Kubernetes and save the changes.
5. Docker Desktop will start the local Kubernetes cluster.

after start the docker desktop kubernetes cluster, you will see the information like below
```bash
deployment.apps/translation-service created
```

6. check the pod is running
```bash
kubectl get deployments
kubectl get pods
```
If successful, you should see the pod is running like below
```bash
NAME                                   READY   STATUS    RESTARTS   AGE
translation-service-769878f4bd-z5g76   1/1     Running   0          7s
```

7. check the service is running
```bash
kubectl get services
```
If successful, you should see the service is running like below
```bash
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   25m
```


