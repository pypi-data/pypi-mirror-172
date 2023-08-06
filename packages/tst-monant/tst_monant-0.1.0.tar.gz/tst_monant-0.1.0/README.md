## This is test repo of MonAnt-Crawler-Parser
[![Build Status](https://travis-ci.com/hucKOder/monant-web-monitoring.svg?token=utNhWnThU8BzcqB33qse&branch=develop)](https://travis-ci.com/hucKOder/monant-web-monitoring)

Crawler using Scrapy with Celery integration

## Requirements

These libraries are needed to be installed
* Scrapy (pip install scrapy, alternative for Windows: conda install -c conda-forge scrapy)
* rabbitmq-server
  * sudo apt-get install rabbitmq-server
  * brew install rabbitmq
* Celery (pip install celery)
* Twisted with newer version (pip3 install git+https://github.com/twisted/twisted.git@trunk)
* Redis

FlaskApi application must be running and provide API.

If needed, set environment variables `MONANT_WEB_MONITORING_CENTRAL_STORAGE_USERNAME` and `MONANT_WEB_MONITORING_CENTRAL_STORAGE_PASSWORD` depending on what API client stored in central data storage database should be used to authorize web monitoring application.

## Running
* Rabbitmq-server must be started (using command {RABBIT_PATH}/sbin/rabbitmq-server) \
* Start celery worker using command (inside folder monant-crawler-parser): celery -A celeryapp.application  worker --loglevel=info
* Run worker.py

