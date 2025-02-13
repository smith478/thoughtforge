## Chat service

One of the core components will be a chat service. We will set this up to use Kubernetes.

### Running the service:

Install NVIDIA Container Toolkit:
```bash
# Add NVIDIA package repositories
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# Install NVIDIA Container Toolkit
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit-base
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

Install the NVIDIA device plugin for Kubernetes:
```bash
# Start Minikube with GPU support and mounted model directory
minikube start --driver=docker --gpus all --memory=24576 --cpus=8 --mount-string="~/huggingface_models/Qwen-Qwen2.5-7B-Instruct:/~/huggingface_models/Qwen-Qwen2.5-7B-Instruct" --mount

# Install NVIDIA device plugin
kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.14.1/nvidia-device-plugin.yml
```

Verify that the GPU is available to the pod:
```bash
# Check if GPU is detected
kubectl get nodes "-o=custom-columns=NAME:.metadata.name,GPU:.status.allocatable.nvidia\.com/gpu"
```

Build and deploy:
```bash
docker build -t chatbot:latest .
kubectl apply -f kubernetes/deployment.yaml
```

Verify the model has been loaded correctly:
```bash
kubectl get pods
# Check the logs
kubectl logs -f deployment/chatbot-deployment

# Verify the mount
kubectl exec -it deployment/chatbot-deployment -- ls /models/qwen
```

To monitor GPU usage:
```bash
# Install nvidia-smi in the pod
kubectl exec -it <pod-name> -- nvidia-smi

# Or on your host machine
watch -n 1 nvidia-smi
```

## Chat on Mac 

### Prerequisites

```bash
brew install docker --cask
brew install kubectl
brew install helm
brew install minikube
```

### Build and Deploy

- Start Kubernetes
```bash
minikube start --driver=docker
```

- Deploy to Kubernetes
```bash
kubectl apply -f ollama-deployment.yaml
kubectl apply -f ollama-service.yaml
```

- Test and verify
```bash
kubectl get deployments
kubectl get pods
```

- Access the service
```bash
# Port-forward to local machine
kubectl port-forward svc/ollama-service 11434:11434
```

## Chat with Web Search

The idea here is to add web search ability to our chatbot, so that when answering questions it also has access to the internet.

This will use the following tools
- DeepSeek R1 distill (for chat)
- Ollama to host the model
- Docker to host the service
- SearXNG for the search engine