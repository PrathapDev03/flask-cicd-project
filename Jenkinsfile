
pipeline {
    agent any

    parameters {
        booleanParam(
            name: 'SIMULATE_HEALTH_FAILURE',
            defaultValue: false,
            description: 'Simulate a failed health check to demonstrate rollback'
        )
    }

    environment {
        DOCKERHUB_REPO = 'prathap03/flask-cicd-demo'
        APP_HOST = '13.239.59.162'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code from GitHub'
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo 'Installing Python dependencies'

                sh '''
                    python3 -m venv .venv
                    .venv/bin/pip install --upgrade pip
                    .venv/bin/pip install -r requirements.txt pytest
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'Executing automated tests'

                sh '''
                    .venv/bin/python -m pytest -v
                '''
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Building Docker image'

                sh '''
                    docker build \
                    -t ${DOCKERHUB_REPO}:${BUILD_NUMBER} \
                    -t ${DOCKERHUB_REPO}:latest .
                '''
            }
        }

        stage('Docker Push') {
            steps {
                echo 'Pushing Docker image to Docker Hub'

                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_TOKEN'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_TOKEN" | docker login \
                        -u "$DOCKER_USER" --password-stdin

                        docker push ${DOCKERHUB_REPO}:${BUILD_NUMBER}
                        docker push ${DOCKERHUB_REPO}:latest

                        docker logout
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying application to AWS EC2'

                sshagent(credentials: ['app-server-ssh']) {
                    sh '''
                        export IMAGE="${DOCKERHUB_REPO}:${BUILD_NUMBER}"

                        export FAILURE="${SIMULATE_HEALTH_FAILURE}"

                        ssh -o StrictHostKeyChecking=no \
                        ubuntu@${APP_HOST} \
                        "IMAGE=$IMAGE FAILURE=$FAILURE bash -s" <<'REMOTE'

                        set -e

                        PREVIOUS_IMAGE=$(docker inspect \
                        --format='{{.Config.Image}}' flask-app 2>/dev/null || true)

                        echo "Previous image: $PREVIOUS_IMAGE"

                        echo "Pulling new image: $IMAGE"

                        docker pull "$IMAGE"

                        docker rm -f flask-app >/dev/null 2>&1 || true

                        echo "Starting new container"

                        if ! docker run -d \
                            --name flask-app \
                            --restart unless-stopped \
                            -p 80:5000 \
                            -e SIMULATE_HEALTH_FAILURE="$FAILURE" \
                            "$IMAGE"; then

                            echo "Container startup failed. Rolling back."

                            if [ -n "$PREVIOUS_IMAGE" ]; then
                                docker run -d \
                                --name flask-app \
                                --restart unless-stopped \
                                -p 80:5000 \
                                "$PREVIOUS_IMAGE"
                            fi

                            exit 1
                        fi

                        echo "Checking application health"

                        for i in $(seq 1 12); do

                            if curl -fsS http://127.0.0.1/health; then
                                echo "Application is healthy"
                                exit 0
                            fi

                            sleep 5
                        done

                        echo "Health check failed. Starting rollback."

                        docker rm -f flask-app >/dev/null 2>&1 || true

                        if [ -n "$PREVIOUS_IMAGE" ]; then

                            echo "Restoring previous image"

                            docker run -d \
                            --name flask-app \
                            --restart unless-stopped \
                            -p 80:5000 \
                            "$PREVIOUS_IMAGE"

                            echo "Rollback completed"

                        else
                            echo "No previous image available"
                        fi

                        exit 1

                        REMOTE
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'CI/CD pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check Jenkins console output.'
        }

        always {
            echo 'Pipeline execution completed.'
        }
    }
}
