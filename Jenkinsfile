
pipeline {
    agent any

    stages {

        // Stage 1: Test SSH Connectivity
        stage('Test Application EC2 SSH') {
            steps {
                echo 'Testing SSH connection to Application EC2'

                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: 'app-server-ssh',
                        keyFileVariable: 'SSH_KEY',
                        usernameVariable: 'SSH_USER'
                    )
                ]) {
                    sh '''
                        ssh -i "$SSH_KEY" \
                            -o BatchMode=yes \
                            -o ConnectTimeout=10 \
                            -o StrictHostKeyChecking=accept-new \
                            "$SSH_USER@172.31.39.12" \
                            "echo 'SSH Authentication Successful'; hostname; whoami"
                    '''
                }
            }
        }

        // Stage 2: Pull Version 1 Image
        stage('Pull Version 1 Image') {
            steps {
                echo 'Pulling Flask Version 1 from Docker Hub'

                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: 'app-server-ssh',
                        keyFileVariable: 'SSH_KEY',
                        usernameVariable: 'SSH_USER'
                    )
                ]) {
                    sh '''
                        ssh -i "$SSH_KEY" \
                            "$SSH_USER@172.31.39.12" \
                            'sudo docker pull prathap03/flask-cicd-demo:v1'
                    '''
                }
            }
        }

        // Stage 3: Deploy Blue Container
        stage('Deploy Blue Container') {
            steps {
                echo 'Starting Version 1 container'

                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: 'app-server-ssh',
                        keyFileVariable: 'SSH_KEY',
                        usernameVariable: 'SSH_USER'
                    )
                ]) {
                    sh '''
                        ssh -i "$SSH_KEY" \
                            "$SSH_USER@172.31.39.12" \
                            'sudo docker rm -f app-blue 2>/dev/null || true;
                             sudo docker run -d \
                             --name app-blue \
                             --restart unless-stopped \
                             -p 127.0.0.1:5001:5000 \
                             prathap03/flask-cicd-demo:v1'
                    '''
                }
            }
        }

        // Stage 4: Health Check Version 1
        stage('Health Check Version 1') {
            steps {
                echo 'Checking Version 1 application health'

                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: 'app-server-ssh',
                        keyFileVariable: 'SSH_KEY',
                        usernameVariable: 'SSH_USER'
                    )
                ]) {
                    sh '''
                        ssh -i "$SSH_KEY" \
                            "$SSH_USER@172.31.39.12" \
                            'for i in $(seq 1 12); do
                                if curl -fsS http://127.0.0.1:5001/health; then
                                    echo "Version 1 is healthy"
                                    exit 0
                                fi

                                echo "Waiting for Version 1..."
                                sleep 5
                             done

                             echo "Version 1 health check failed"
                             sudo docker logs app-blue
                             exit 1'
                    '''
                }
            }
        }

        // Stage 5: Verify Nginx Traffic
        stage('Verify Nginx Traffic') {
            steps {
                echo 'Testing application through Nginx'

                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: 'app-server-ssh',
                        keyFileVariable: 'SSH_KEY',
                        usernameVariable: 'SSH_USER'
                    )
                ]) {
                    sh '''
                        ssh -i "$SSH_KEY" \
                            "$SSH_USER@172.31.39.12" \
                            'sudo nginx -t &&
                             curl -fsS http://127.0.0.1/ &&
                             echo &&
                             curl -fsS http://127.0.0.1/health'
                    '''
                }
            }
        }

        // Stage 6: Pull Version 2 Image
        stage('Pull Version 2 Image') {
            steps {
                echo 'Pulling Flask Version 2 from Docker Hub'

                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: 'app-server-ssh',
                        keyFileVariable: 'SSH_KEY',
                        usernameVariable: 'SSH_USER'
                    )
                ]) {
                    sh '''
                        ssh -i "$SSH_KEY" \
                            "$SSH_USER@172.31.39.12" \
                            'sudo docker pull prathap03/flask-cicd-demo:v2'
                    '''
                }
            }
        }

        // Stage 7: Deploy Green Container
        stage('Deploy Green Container') {
            steps {
                echo 'Deploying Flask Version 2 as Green'

                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: 'app-server-ssh',
                        keyFileVariable: 'SSH_KEY',
                        usernameVariable: 'SSH_USER'
                    )
                ]) {
                    sh '''
                        ssh -i "$SSH_KEY" \
                            "$SSH_USER@172.31.39.12" \
                            'sudo docker rm -f app-green 2>/dev/null || true;
                             sudo docker run -d \
                             --name app-green \
                             --restart unless-stopped \
                             -p 127.0.0.1:5002:5000 \
                             prathap03/flask-cicd-demo:v2'
                    '''
                }
            }
        }

        // Stage 8: Health Check Version 2
        stage('Health Check Version 2') {
            steps {
                echo 'Checking Green Version 2 application health'

                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: 'app-server-ssh',
                        keyFileVariable: 'SSH_KEY',
                        usernameVariable: 'SSH_USER'
                    )
                ]) {
                    sh '''
                        ssh -i "$SSH_KEY" \
                            -o BatchMode=yes \
                            "$SSH_USER@172.31.39.12" \
                            'bash -s' <<'REMOTE_SCRIPT'

for i in $(seq 1 12); do

    RESPONSE=$(curl -fsS --max-time 5 \
        http://127.0.0.1:5002/health 2>/dev/null || true)

    echo "Green health response: $RESPONSE"

    if [ -n "$RESPONSE" ]; then

        if printf '%s' "$RESPONSE" | python3 -c '
import sys
import json

data = json.load(sys.stdin)

if data.get("status") != "healthy":
    sys.exit(1)

if str(data.get("version")) != "2.0":
    sys.exit(1)
'; then

            echo "Version 2 is healthy"
            echo "Green deployment health check successful"
            exit 0

        fi
    fi

    echo "Waiting for Version 2..."
    sleep 5

done

echo "Green deployment health check failed"
sudo docker logs app-green
exit 1

REMOTE_SCRIPT
                    '''
                }
            }
        }
    } 
} 
