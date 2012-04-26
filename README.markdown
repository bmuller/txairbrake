# txairbrake: Airbrake error reporting for Twisted
[Airbrake](http://www.airbrake.io) provides a service that aggregates errors from applications.  This project is specifically designed for asynchronous [Python Twisted](http://twistedmatrix.com) code to send exceptions to an airbrake server.  Unlike traditional synchronous Python code, there can be no blocking in the error reporting in a Twisted project.  This library connects to the remote server in a non-blocking fashion.

## Installation

    git clone https://github.com/bmuller/txairbrake
    cd txairbrake
    python setup.py install

## Usage

    # import the observer
    from txairbrake.observers import AirbrakeLogObserver

    # Create observer.  Params are api key, environment, and use SSL.  The last two are optional.
    ab = AirbrakeLogObserver("mykey", "production", True)

    # start observing errors
    ab.start()


# Errbit
Airbrake costs money.  If you don't want to spend money, consider using [Errbit](https://github.com/errbit/errbit), which is free and can run for free on Heroku.  If you do end up using an alternative server, the observer constructor takes a final parameter that is the hostname of your airbrake-compliant server.
