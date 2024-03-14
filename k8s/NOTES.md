Install the NVIDIA Device Plugin for Kubernetes if cluster uses NVIDIA GPUs. This plugin allows Kubernetes to schedule GPU resources:

```bash
kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/master/nvidia-device-plugin.yml
```