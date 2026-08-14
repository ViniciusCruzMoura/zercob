pipeline {
    agent {
        label 'prod && srv004036'
    }

    environment {
        env_file = credentials('sebrae_integracoes_env')
    }

    stages {
        stage('Build') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Deploy') {
            steps {
                sh 'cat $env_file > .env'
                sh 'docker compose down'
                sh 'docker compose up -d'
            }
        }
    }
}
