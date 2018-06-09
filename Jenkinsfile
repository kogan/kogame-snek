// projectName is sanitised by docker-compose
// only use [a-zA-Z0-9] otherwise they'll be silently stripped and docker cp will fail
def projectName
try {
  projectName = "kogame_pr_${CHANGE_ID}build${BUILD_NUMBER}"
} catch (groovy.lang.MissingPropertyException e) {
  projectName = "kogame_${BRANCH_NAME}build${BUILD_NUMBER}"
}

def withGithubNotify(context, closure) {
  final githubNotifyCreds = 'kogan-bot-cf-userpw-token'
  def everythingIsFine = true
  try {
    githubNotify(context: context, status: 'PENDING', credentialsId: githubNotifyCreds)
    closure.call()
  } catch (e) {
    everythingIsFine = false
    throw e
  } finally {
    final status = (everythingIsFine ? 'SUCCESS' : 'FAILURE')
    githubNotify(context: context, status: status, credentialsId: githubNotifyCreds)
  }
}

node {
  stage('build') {
    checkout scm
    sh 'git clean -dfx || true'
    sh 'pipenv install --dev --python 3.6'
  }

  stage('flake8') {
    withGithubNotify('flake8') {
      timeout(time: 2, unit: 'MINUTES') {
        try {
          sh 'pipenv run flake8 --tee --output-file=flake8.log'
        } finally {
          step([$class: 'WarningsPublisher',
            parserConfigurations: [
              [parserName: 'flake8', pattern: 'flake8.log']
            ],
            failedTotalAll: '0',
            usePreviousBuildAsReference: false
          ])
        }
      }
    }
  }

  stage('isort') {
    withGithubNotify('isort') {
      timeout(time: 2, unit: 'MINUTES') {
        sh 'pipenv run isort --check-only --diff --skip .venv --skip node_modules --skip migrations'
      }
    }
  }

  stage('eslint') {
    withGithubNotify('eslint') {
      timeout(time: 5, unit: 'MINUTES') {
        sh 'npm install --dev'
        try {
          sh './node_modules/.bin/eslint -c ".eslintrc" -f checkstyle $(git diff origin/develop... --name-only -- \'*.js\' \'*.jsx\') > "./checkstyle-result.xml"'
        } finally {
          checkstyle canComputeNew: false, canRunOnFailed: true, defaultEncoding: '', healthy: '', pattern: '**/checkstyle-result.xml', unHealthy: ''
        }
      }
    }
  }
}
