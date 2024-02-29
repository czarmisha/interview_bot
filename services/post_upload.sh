#!/bin/bash
if systemctl stop interview_bot.service ; then
    sudo cp /home/ubuntu/interview_bot/services/interview_bot.service /etc/systemd/system/
else
    echo "No interview_bot.service found in system, now will creating"
    sudo cp /home/ubuntu/interview_bot/services/interview_bot.service /etc/systemd/system
fi
sudo systemctl daemon-reload
sudo systemctl enable interview_bot.service
sudo systemctl start interview_bot.service
rm  /home/ubuntu/interview_bot.tar