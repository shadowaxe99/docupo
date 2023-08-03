```groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                sh 'docker build -t docurepo:latest ./deployment'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
                // Add your test scripts here
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
                sh 'kubectl apply -f ./deployment/kubernetes_config.yaml'
            }
        }
    }

    post {
        failure {
            echo 'Build failed!'
        }
        success {
            echo 'Build succeeded!'
        }
    }
}
```