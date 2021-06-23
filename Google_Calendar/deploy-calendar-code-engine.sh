#!/bin/bash

ic target -r us-south
ic target -g default
ic ce proj select -n Utils

REV=$(date +"%y-%m-%d-%H-%M-%S")
echo ${REV}

ic ce app update -n calendar -i docker.io/kineticsquid/calendar:latest --rn ${REV} --min 1
ic ce rev list --app calendar
ic ce app events --app calendar
ic ce app logs --app calendar
