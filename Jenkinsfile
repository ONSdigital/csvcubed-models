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
            steps {
                sh 'poetry install'
            }
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
        stage('Set dev version') {
            // when {
            //     branch 'main'
            // }
            steps {
                // This runs when we're not building a release or release candidate
                // It sets the version of the project to something containing the decimalised version of the
                // git commit id so that the package can be automatically deployed to testpypi.

                sh 'revision="$(git rev-parse HEAD | tr \'[:lower:]\' \'[:upper:]\')"; decimal_rev=$(echo "obase=10; ibase=16; $revision" | bc); poetry version "0.1.0-dev$decimal_rev"'
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
        stage('Publish to Test-pypi') {
            when {
                branch 'main'
            }
            steps {
                script {
                    sh "twine check dist/csvcubed_models*.whl"

                    withCredentials([usernamePassword(credentialsId: 'testpypi-robons', usernameVariable:'TWINE_USERNAME', passwordVariable: 'TWINE_PASSWORD')]) {
                        sh 'twine upload -r testpypi dist/csvcubed_models*.whl'
                    }
                }
            }
        }
        stage('Publish to Pypi') {
            when {
                buildingTag()
                tag pattern: "v\\d+\\.\\d+\\.\\d+(-RC\\d)?", comparator: "REGEXP"
            }
            steps {
                script {
                    sh "twine check dist/csvcubed_models*.whl"

                    withCredentials([usernamePassword(credentialsId: 'pypi-robons', usernameVariable:'TWINE_USERNAME', passwordVariable: 'TWINE_PASSWORD')]) {
                        sh 'twine upload dist/csvcubed_models*.whl'
                    }
                }
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
