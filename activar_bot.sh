#!/bin/bash
sudo systemctl stop zafiro_bot.service
sudo cp services/zafiro_bot.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable zafiro_bot.service
sudo systemctl start zafiro_bot.service
sudo systemctl status zafiro_bot.service