#!/bin/bash
sudo systemctl stop zafiro_audio.service
sudo cp services/zafiro_audio.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable zafiro_audio.service
sudo systemctl start zafiro_audio.service
sudo systemctl status zafiro_audio.service