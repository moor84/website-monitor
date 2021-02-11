# Website Monitor

## Overview

Website Monitor is a simple application that demostraits working with Aiven Kafka and Aiven PostgreSQL services.

The application monitors website availability over the
network, produces metrics about this and stores in an Aiven PostgreSQL database.

## Requirements

- Python 3.7+

- Running Aiven Kafka instance

- Running Aiven PostgreSQL database instance

## Installation and general use

### Installation

Simply clone this repository and run pip install:

```
git clone git@github.com:moor84/website-monitor.git
cd website-monitor
pip install ./
```

Set up an Aiven Kafka instance and an Aiven PostgreSQL instance.
Create a database schema by applying the `schema.sql` file.

Then copy `config.json.example` and adjust the config file.

The application consists of two parts - Checker and Writer - that communicate through Kafka topic.

### Checker

To run the Checker:

```
monitor checker --config=config.json --url=https://www.example.com
```

Optionally, set a pattern to check if it is present on page:

```
monitor checker --config=config.json --url=https://www.ya.ru --pattern='yandex'
```

It is possible to run multiple checkers at a time with different parameters.

### Writer

To run the Writer:

```
monitor writer --config=config.json
```
It is possible to run multiple writers at a time thus scaling the service.

## Contributing

### Quick Start

Create a local virtual environment and install dependencies:

```
virtualenv -p python3 .env
. .env/bin/activate
pip install -r requirements.txt
```

### Running unit-tests

```
pytest --cov=website_monitor tests
```

### Running linter check

```
mypy website_monitor
```

## Possible improvements

- Intergration testing

- Graceful shutdown

- Extendable DB schema (to easily add new metrics)

- Docker integration

- Automatically create a DB schema on the first run
