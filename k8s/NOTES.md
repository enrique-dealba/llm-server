Install the NVIDIA Device Plugin for Kubernetes if cluster uses NVIDIA GPUs. This plugin allows Kubernetes to schedule GPU resources:

```bash
kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/master/nvidia-device-plugin.yml
```

## Setting up and Running the Actual LLM Server

### Step 1: Setting up the environment
1.1. Commands to run
```shell
microk8s helm uninstall llm-server

microk8s kubectl delete pvc llm-server-pvc
microk8s kubectl delete pv llm-server-pv

docker pull edealba2/llm-server:latest

microk8s kubectl apply -f k8s/pv.yaml
microk8s kubectl get pv

microk8s helm install llm-server ./helm
OR
microk8s helm upgrade --install llm-server ./helm

microk8s kubectl get pods
microk8s kubectl logs -f <pod-name>
microk8s kubectl describe pod <pod-name>

microk8s helm uninstall llm-server
```

## Setting up and Running the Mock LLM Server

### Step 1: Setting up the environment
1.1. Navigate to LLM server codebase directory

1.2. cd into the `k8s` directory

1.3. Export the NEXUS tokens required for the Kubernetes Dockerfile:
```shell
export NEXUS_USER=<your-nexus-username>
export NEXUS_TOKEN=<your-nexus-token>
```

### Step 2: Building the Docker image
2.1 Build Docker image using the provided k8s Dockerfile:
```shell
docker build -t llm-server:mock . --build-arg NEXUS_USER=$NEXUS_USER --build-arg NEXUS_TOKEN=$NEXUS_TOKEN
```

### Step 3: Setting up Minikube
3.1. Install Minikube by running:
```shell
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/
```
3.2. Start Minikube with the Docker driver:
```shell
minikube start --driver=docker
```

### Step 4: Deploying the Helm chart
4.1. cd to the `helm` directory:
```shell
cd ../helm
```
4.2. Load the Docker image into Minikube's Docker daemon:
```shell
minikube image load llm-server:mock
```
4.3. Install the Helm chart:
```shell
helm install llm-server .
```

### Step 5: Verifying the deployment
5.1. Check if the pods and services are running, and if the PersistentVolumeClaim is bound:
```shell
kubectl get pods
kubectl get services
kubectl get pvc
```

### Step 6: Accessing the LLM server
6.1. Port-forward the `llm-server` service to access it locally:
```shell
kubectl port-forward service/llm-server 8080:5000
```
6.2. Open a new terminal window and send a test request to the LLM server:
```shell
curl -X POST -H "Content-Type: application/json" -d '{"text": "Your text here"}' http://localhost:8080/generate
```

### Step 7: Cleaning up resources
7.1. Stop the port-forwarding process by pressing `Ctrl+C` in the terminal window where you ran the kubectl port-forward command.

7.2. Uninstall the Helm chart:
```shell
helm uninstall llm-server
```
7.3. Double-check if there are any remaining resources in the default namespace:
```shell
kubectl get all
kubectl get pv
kubectl get pvc
```
7.4. Stop and delete the Minikube cluster:
```shell
minikube stop
minikube delete
```
