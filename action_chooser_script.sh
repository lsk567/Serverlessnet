#!/bin/bash

wsk -i action create myAction openwhisk_actions/action.js
wsk -i action create action2 openwhisk_actions/action.js
