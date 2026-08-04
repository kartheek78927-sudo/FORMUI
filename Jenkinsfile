pipeline {
    agent any

    parameters {
        string(
            name: 'IMAGE_TAG',
            defaultValue: 'manual-build',
            description: 'Docker Image Tag'
        )

        string(
            name: 'DOCKER_REPO',
            defaultValue: 'manjunath123456789/hospitalform',
            description: 'Docker Hub Repository'
        )
    }

    environment {
        // Jenkins Credentials ID
        DOCKER_CREDENTIALS_ID = 'dockerhub-creds'

        // Docker Variables
        DOCKER_REPO = "${params.DOCKER_REPO}"
        IMAGE_TAG = "${params.IMAGE_TAG}"
        IMAGE_NAME = "${params.DOCKER_REPO}:${params.IMAGE_TAG}"

        // Helm
        HELM_CHART = "formui-chart"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    echo "Building Docker Image..."
                    docker build -t ${IMAGE_NAME} .
                '''
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: "${DOCKER_CREDENTIALS_ID}",
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    '''
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                sh '''
                    echo "Pushing Docker Image..."
                    docker push ${IMAGE_NAME}
                '''
            }
        }

        stage('Helm Lint') {
            steps {
                sh '''
                    helm lint ${HELM_CHART}
                '''
            }
        }

        stage('Package Helm Chart') {
            steps {
                sh '''
                    helm package ${HELM_CHART}
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline Completed Successfully."
        }

        failure {
            echo "Pipeline Failed."
        }

        always {
            sh 'docker logout || true'
            cleanWs()
        }
    }
}
