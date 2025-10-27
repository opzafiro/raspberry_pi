#!/bin/bash
sudo systemctl stop zafiro_prueba.service
sudo cp services/zafiro_prueba.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable zafiro_prueba.service
sudo systemctl start zafiro_prueba.service
sudo systemctl status zafiro_prueba.service