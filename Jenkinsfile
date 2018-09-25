elifeLibrary {
    def commit
    stage 'Checkout', {
        checkout scm
        commit = elifeGitRevision()
    }

    stage 'Install', {
        sh './install.sh'
    }

    stage 'Run tests', {
        elifeLocalTests './project_tests.sh'
    }
}
