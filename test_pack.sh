#!/bin/sh

zip -q -r amiyabot-hsyhhssyy-functions-gui-1.0.zip *
rm -rf ../../amiya-bot-v6/plugins/amiyabot-hsyhhssyy-functions-gui-*
mv amiyabot-hsyhhssyy-functions-gui-*.zip ../../amiya-bot-v6/plugins/
docker restart amiya-bot 