pipeline {
  agent any

  parameters {
    string(name: 'IMAGE_TAG', defaultValue: 'manual-build', description: 'Docker image tag to build and push')
    string(name: 'DOCKER_REPO', defaultValue: 'manjunath123456789/hospitalform', description: 'Docker Hub repository')
  }

  environment {
    DOCKER_CREDENTIALS_ID = 'dockerhub-creds'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker image') {
      steps {
        sh "docker build -t ${params.DOCKER_REPO}:${params.IMAGE_TAG} ."
      }
    }

    stage('Push to Docker Hub') {
      steps {
        withCredentials([usernamePassword(credentialsId: env.DOCKER_CREDENTIALS_ID, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh '''
            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
            docker push ${DOCKER_REPO}:${IMAGE_TAG}
          '''
        }
      }
    }

    stage('Package Helm Chart') {
      steps {
        sh 'helm lint formui-chart'
        sh 'helm package formui-chart'
      }
    }
  }
}
