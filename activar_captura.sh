#!/bin/bash
sudo systemctl stop zafiro_proceso_camara.service
sudo cp services/zafiro_proceso_camara.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable zafiro_proceso_camara.service
sudo systemctl start zafiro_proceso_camara.service
sudo systemctl status zafiro_proceso_camara.service


