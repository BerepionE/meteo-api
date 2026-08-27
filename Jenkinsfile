pipeline {
    agent any

    environment {
        IMAGE = "eberepion/meteo-api"
        TAG   = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Tester') {
            steps {
                sh 'docker build --target test -t meteo-api:test-$TAG .'
            }
        }
        stage('Construire') {
            steps {
                sh 'docker build -t $IMAGE:$TAG -t $IMAGE:latest .'
            }
        }
        stage('Publier') {
            steps {
                withCredentials([usernamePassword(
                        credentialsId: 'docker-hub',
                        usernameVariable: 'REGISTRE_USER',
                        passwordVariable: 'REGISTRE_PASS')]) {
                    sh '''
                        echo "$REGISTRE_PASS" | docker login -u "$REGISTRE_USER" --password-stdin
                        docker push $IMAGE:$TAG
                        docker push $IMAGE:latest
                    '''
                }
            }
        }
        stage('Deployer') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-kind', variable: 'KUBECONFIG')]) {
                    sh '''
                        kubectl set image deployment/meteo-api api=$IMAGE:$TAG || kubectl create deployment meteo-api --image=$IMAGE:$TAG --port=8000
                        kubectl rollout status deployment/meteo-api --timeout=300s
                        kubectl get pods -l app=meteo-api
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "SUCCES : ${env.IMAGE}:${env.TAG} est deploye !"
        }
        failure {
            echo "ECHEC sur le pipeline."
        }
        always {
            sh 'docker logout || true'
            sh 'docker image prune -f || true'
        }
    }
}
