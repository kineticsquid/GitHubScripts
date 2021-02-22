#!/usr/bin/env bash

#Instructions for accessing production:
#

bx ibmcloud login --sso -a https://cloud.ibm.com
echo "=========="
echo "Choose production environment (PPRD)"
echo "=========="
~/kubectl-helper-master/setup.sh
echo "=========="
echo "Choose region"
echo "=========="
~/kubectl-helper-master/switch.sh
source /tmp/cluster_config_output

kubectl get pods -n {namespace} | awk '{print $1}' | kubectl describe pod | grep "Image ID" | awk '{print $3}' | sort | uniq