# FORMUI CI/CD Setup

This project already contains a Flask app, a Dockerfile, and a Helm chart. The recommended flow is:

1. Push code to GitHub.
2. GitHub Actions builds and publishes a Docker image.
3. Jenkins can be triggered manually to build and push another image tag.
4. Argo CD syncs the Helm chart to your Kubernetes cluster.

## 1) GitHub Actions

Set these repository secrets in GitHub:

- DOCKER_USERNAME
- DOCKER_PASSWORD

The workflow in .github/workflows/ci.yml will build the image on every push to main and push it to Docker Hub.

## 2) Jenkins

Install these Jenkins plugins:

- Docker Pipeline
- Git
- Pipeline

Create a Jenkins credential with ID dockerhub-creds using your Docker Hub username/password.

Create a Pipeline job that points to this repository and uses the Jenkinsfile.

Run the job with parameters:

- IMAGE_TAG: for example manual-build
- DOCKER_REPO: your Docker Hub repository

## 3) Argo CD

Install Argo CD in your cluster, then apply the manifest in argocd/application.yaml after replacing the GitHub repo URL.

Example:

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl apply -f argocd/application.yaml
```

## 4) Kubernetes notes

Make sure the image repository in formui-chart/values.yaml matches the image you publish.

If you want Argo CD to use a specific image tag, update the chart values accordingly.
