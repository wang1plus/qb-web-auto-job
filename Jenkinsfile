#!/usr/bin/env groovy
pipeline {
  agent any
  stages{
    stage('first') {
      steps {
        echo 'hello from github'
        sh 'pwd'
        echo pwd()
      }
    }
    stage('echo code'){
      steps {
        main_py_path = '${env.WORKSPACE}/src/main.py'

        if(fileExists(main_py_path) == true){
          echo main_py_path
          sh 'ls -al ${main_py_path}'
          cat main_py_path
        }
      }
    }
  }
}