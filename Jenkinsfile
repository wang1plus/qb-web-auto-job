#!/usr/bin/env groovy
pipeline {
  agent any
  stages{
    stage('first') {
      steps {
        echo 'hello from github'
        sh 'pwd'
        sh 'ls -al'
      }
    }
    stage('echo code'){
      steps {
        cat src/main.py
      }
    }
  }
}