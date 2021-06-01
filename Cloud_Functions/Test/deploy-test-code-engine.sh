#!/bin/bash

ic target -r us-south
ic target -g default
ic ce proj select -n Test

REV=$(date +"%y-%m-%d-%H-%M-%S")
echo ${REV}

ic ce app update -n test --min 1 -i docker.io/kineticsquid/test:latest --rn ${REV}
ic ce rev list --app test
ic ce app events --app test
ic ce app logs --app test

