#!/usr/bin/env groovy
pipeline {
  agent any
  stages{
    stage('first') {
      steps {
        echo 'hello from github'
        ls -al
      }
      steps {
        cat ./src/main.py
      }
    }
  }
}