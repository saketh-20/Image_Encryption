def call(Map config = [:]) {

    pipeline {
        agent any

        stages {

            stage('Checkout') {
                steps {
                    git url: config.repoUrl, branch: config.branch
                }
            }

            stage('Build') {
                steps {
                    echo 'Build step...'
                }
            }

            stage('Test') {
                steps {
                    echo 'Test step...'
                }
            }

            stage('Deploy') {
                steps {
                    echo 'Deploy step...'
                }
            }

        }
    }
}
