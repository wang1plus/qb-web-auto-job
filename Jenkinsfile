#!/usr/bin/env groovy
pipeline {
  agent any
  stages{
    stage('first') {
      steps {
        echo 'hello from github'
        sh 'ls -al'
      }
    }
    staget('echo code'){
      steps {
        cat src/main.py
      }
    }
  }
}