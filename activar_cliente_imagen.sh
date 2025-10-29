#!/bin/bash
sudo systemctl stop zafiro_imagen.service
sudo cp services/zafiro_imagen.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable zafiro_imagen.service
sudo systemctl start zafiro_imagen.service
sudo systemctl status zafiro_imagen.service



