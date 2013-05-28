# txairbrake: Airbrake error reporting for Twisted
[![Build Status](https://secure.travis-ci.org/bmuller/txairbrake.png?branch=master)](https://travis-ci.org/bmuller/txairbrake)

[Airbrake](http://www.airbrake.io) provides a service that aggregates errors from applications.  This project is specifically designed for asynchronous [Python Twisted](http://twistedmatrix.com) code to send exceptions to an airbrake server.  Unlike traditional synchronous Python code, there can be no blocking in the error reporting in a Twisted project.  This library connects to the remote server in a non-blocking fashion.

## Installation

    easy_install txairbrake

## Usage

    # import the observer
    from txairbrake.observers import AirbrakeLogObserver

    # Create observer.  Params are api key, environment, and use SSL.  The last two are optional.
    ab = AirbrakeLogObserver("mykey", "production", True)

    # start observing errors
    ab.start()

### Controlling how HTTP Requests are made.

txairbrake uses [twisted.web.client.Agent](http://twistedmatrix.com/documents/current/api/twisted.web.client.Agent.html)
for making HTTP requests.  This gives you the user a great deal of control over how the HTTP requests are made, including
if persistent connections should be used, and if requests should be made through a an HTTP proxy.

#### Persistent Connections

    # import observer, reactor, and client classes.
    from txairbrake.observers import AirbrakeLogObserver
    from twisted.internet import reactor
    from twisted.web.client import Agent, HTTPConnectionPool

    # Create a persistent connection pool and a new Agent instance.
    pool = HTTPConnectionPool(reactor, persistent=True)
    agent = Agent(reactor, pool)

    # Set up an observer to use the preconfigured Agent.
    ab = AirbrakeLogObserver("mykey", "production", True, agent=agent)

    # start observing errors.
    ab.start()

#### HTTP Proxy

    # import observer, reactor, and client classes.
    from txairbrake.observers import AirbrakeLogObserver
    from twisted.internet import reactor
    from twisted.internet.endpoints import TCP4ClientEndpoint
    from twisted.web.client import ProxyAgent

    # Create a client endpoint pointed at a proxy on localhost.
    proxy_endpoint = TCP4ClientEndpoint(reactor, "localhost", 8000)

    # Create a proxy agent that will use the client endpoint.
    agent = ProxyAgent(proxy_endpoint)

    # Set up an observer to use the preconfigured ProxyAgent.
    ab = AirbrakeLogObserver("mykey", "production", True, agent=agent)

    # start observing errors.
    ab.start()

# Errbit
Airbrake costs money.  If you don't want to spend money, consider using [Errbit](https://github.com/errbit/errbit), which is free and can run for free on Heroku.  If you do end up using an alternative server, the observer constructor takes a final parameter that is the hostname of your airbrake-compliant server.
