# Powerful Pipes Watcher - Multi-broker watcher tool with the power of UNIX Pipes

![License](https://img.shields.io/badge/License-Apache2-SUCCESS)
![Pypi](https://img.shields.io/pypi/v/powerful-pipes-watch-bus)
![Versions](https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10-blue)

![Logo](https://raw.githubusercontent.com/42Crunch/powerful-pipes-bus-watcher/main/docs/logo-250x250.png)

# Index

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Install](#install)
- [Quick Start](#quick-start)
  - [WatchBus](#watchbus)
  - [SendBus](#sendbus)
  - [As a Python library](#as-a-python-library)
- [Supported brokers](#supported-brokers)
  - [Redis examples](#redis-examples)
    - [Redis Simple Queue Listener](#redis-simple-queue-listener)
    - [Redis Pub / Sub](#redis-pub--sub)
    - [Redis Streams](#redis-streams)
- [Authors](#authors)
- [License](#license)
- [Contributions](#contributions)
- [Acknowledgements](#acknowledgements)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


In a nutshell `Powerful Pipes Watcher` is a multi broker watcher tool that connect them with UNIX pipes.

# Install

```bash
> pip install powerful-pipes-watch-bus 
```

# Quick Start

## WatchBus

Powerful Pipes Watcher read from a broker queue and re-send received data to the UNIX pipeline.

**Example**

```bash
> watch-bus -c redis:// -q my-queue 
```

Above command will connect to the localhost Redis at default port, at database number 1, and will listen for `my-queue` queue.

**Example with multiple queues**

```bash
> watch-bus -c redis:// -q my-queue -q second-queue 
```

With this command watch-bus will listen from two queues events.


## SendBus

Powerful Pipes SendBus read from stdin and re-send received JSON data to the Broker queue(s).

**Example**

```bash
> cat data.json | send-bus -c redis:// -q my-queue 
```

Above command will connect to the localhost Redis at default port, at database number 1, and will listen for `my-queue` queue.

**Example with multiple queues**

```bash
> cat data.json | send-bus -c redis:// -q my-queue -q second-queue 
```

With this command sendBus will send data to two broker queues.

## As a Python library

You also can use ``Powerful Pipes Watcher`` as a Python library in your Python code:

```python
from powerful_pipes_watch_bus import connect_bus

def main():
  redis_connection = connect_bus("redis+pubsub://localhost:6379/?db=0&channel=my-channel")
  
  for message in redis_connection.read_json_messages():
    redis_connection.send_json_message(message, "my-other-queue")

if __name__ == "__main__":
  main()
```

# Supported brokers

Currently, supported brokers are:

- Redis Pub/Sub
- Redis Streams
- Redis simple Queue listener

>   We'll be happy if you want to contribute adding new brokers! :)

## Redis examples

### Redis Simple Queue Listener

Bus connections for Redis should look like:

`redis://[[user]:[password]@][host][:port][/?db=INTEGER][&queue=STRING]]`

Default values:

- user: Null
- password: Null
- Host: 127.0.0.1
- port: 6379
- db: 1
- queue: default

### Redis Pub / Sub

Bus connections for Redis should look like:

`redis+pubsub://[[user]:[password]@][host][:port][/?[db=INTEGER][&channel=STRING]]`

> channel is the pub/sub channel to listen for.

Default values:

- user: Null
- password: Null
- Host: 127.0.0.1
- port: 6379
- db: 1
- channel: default

### Redis Streams

Bus connections for Redis should look like:

`redis+streams://[[user]:[password]@][host][:port]/?stream=STRING[&db=INTEGER][&group=STRING][&consumer=STRING][&timeout=INTEGER][&batch_size=INTEGER]`

This mode can works as a consumer or as a producer, depending on the parameters.

**Consumer**

If you want to use the Redis Streams as a consumer, you should specify the `group` and `consumer` parameters.

**Producer**

If you want to use the Redis Streams as a producer, you should specify ONLY the `stream` parameter.

**Mandatory parameters**

- stream: The stream name to listen for.

Default values:

- user: Null
- password: Null
- Host: 127.0.0.1
- port: 6379
- db: 1
- consumer: "auto" (will be generated automatically)

# Authors

Powerful Pipes was made by 42Crunch Research Team:

- [jc42](https://github.com/jc42c)
- [cr0hn](https://github.com/cr0hn>)


# License

Powerful Pipes is Open Source and available under the [AGPLv3+](https://github.com/42crunch/powerful-pipes-bus-watcher/blob/main/LICENSE).

# Contributions

Contributions are very welcome. See [CONTRIBUTING.md](https://github.com/42crunch/powerful-pipes-bus-watcher/blob/main/CONTRIBUTING.md>) or skim existing tickets to see where you could help out.

# Acknowledgements

Project logo thanks to [Camera control vector created by upklyak](https://www.freepik.com/vectors/camera-control).

