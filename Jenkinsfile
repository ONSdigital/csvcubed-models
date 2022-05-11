pipeline {
    agent {
        dockerfile {
            args '-u root -v /var/run/docker.sock:/var/run/docker.sock'
            reuseNode true
        }
    }
    stages {
        stage('Setup') {
            // Make sure that poetry installs the local package.
            sh 'poetry install'
        }
        stage('Pyright') {
            when { not { buildingTag() } }
            steps {
                sh 'poetry run pyright . --lib'
            }
        }
        stage('Test') {
            when { not { buildingTag() } }
            steps {
                script {
                    try {
                        dir('tests/unit') {
                            sh "poetry run pytest --junitxml=pytest_results_models.xml"
                        }
                    } catch (ex) {
                        echo "An error occurred when testing: ${ex}"
                        stash name: 'test-results', includes: '**/test-results.json,**/*results*.xml' // Ensure test reports are available to be reported on.
                        throw ex
                    }

                    stash name: 'test-results', includes: '**/test-results.json,**/*results*.xml' // Ensure test reports are available to be reported on.
                }
            }
        }
        stage('Tox') {
            when { 
                buildingTag()
                tag pattern: "v\\d+\\.\\d+\\.\\d+(-RC\\d)?", comparator: "REGEXP"
            }
            agent {
                docker { image 'gsscogs/pythonversiontesting' }
            }
            steps {
                script {
                    try {
                        sh 'tox'
                    } catch (ex) {
                        echo "An error occurred testing with tox: ${ex}"
                        stash name: 'tox-test-results', includes: '**/tox-test-results-*.json,**/*results*.xml'
                        throw ex
                    }
                    // Ensure test reports are available to be reported on.
                    stash name: 'tox-test-results', includes: '**/tox-test-results-*.json,**/*results*.xml'
                }
            }
        }
        stage('Package') {
            steps {
                dir('csvcubed-models') {
                    sh 'poetry build'
                }

                stash name: 'wheels', includes: '**/dist/*.whl'
            }
        }
    }
    post {
        always {
            script {
                try {
                    unstash name: 'test-results'
                } catch (Exception e) {
                    echo 'test-results stash does not exist'
                }

                try {
                    unstash name: 'tox-test-results'
                } catch (Exception e) {
                    echo 'tox-test-results stash does not exist'
                }

                cucumber fileIncludePattern: '**/test-results.json'
                cucumber fileIncludePattern: '**/tox-test-results-*.json'
                junit allowEmptyResults: true, testResults: '**/*results*.xml'

                try {
                    unstash name: 'wheels'
                } catch (Exception e) {
                    echo 'wheels stash does not exist'
                }

                archiveArtifacts artifacts: '**/dist/*.whl, **/docs/_build/html/**/*, **/external-docs/site/**/*, **/test-results.json, **/tox-test-results-*.json, **/*results*.xml', fingerprint: true

                // Set more permissive permissions on all files so future processes/Jenkins can easily delete them.
                sh 'chmod -R ugo+rw .'
                // Clean up any unwanted files lying about.
                sh "git clean -fxd --exclude='.venv'"
            }
        }
    }
}
