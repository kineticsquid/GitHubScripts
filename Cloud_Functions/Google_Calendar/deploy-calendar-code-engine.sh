#!/bin/bash

ibmcloud target -r us-south
ibmcloud target -g default
ibmcloud ce project select --name Utils

ibmcloud ce application update --name calendar --image docker.io/kineticsquid/calendar:latest
ibmcloud ce revision list --application calendar
ibmcloud ce application events --application calendar
ibmcloud ce application logs --app calendar
