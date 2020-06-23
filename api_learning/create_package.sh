#!bin/bash
zip package.zip slack_topic_slack_module.py
cd ./env/lib/python3.7/site-packages/
zip -r ../../../../package.zip *
