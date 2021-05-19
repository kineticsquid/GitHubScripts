#!/bin/bash

ibmcloud target -r us-south
ibmcloud target -g default
ibmcloud ce project select --name Test

ibmcloud ce application update --name test --image docker.io/kineticsquid/test:latest
ibmcloud ce revision list --application test
ibmcloud ce application events --application test
ibmcloud ce application logs --app test

