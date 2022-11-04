#!/bin/bash
docker build -t miniapp/trade:0.1 -t miniapp/trade:latest -f docker/trade/Dockerfile .
