# Kogame - Snek

[![Build Status](https://travis-ci.org/kogan/kogame-snek.svg?branch=master)](https://travis-ci.org/kogan/kogame-snek)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Kogame - pronounced with 3 syllables (Koh-gah-mee) - is a Django Channels real-time or turn-based game platform.

Snek is a multiplayer version of the famous game `snake`. It uses django and channels
for the game engine on the server, and react to render the actual game state on
the client.

Snek is one of the games we created as part of our Kogan hackday. It's gone through
a few changes to get it ready for public consumption.

We've deployed it to Heroku at https://kogame-snek.herokuapp.com/ if you'd like
to give it a go.

Note: this project is a work in progress. It has many rough edges. If you'd like
to contribute, there are a number of [https://github.com/kogan/kogame-snek/issues](issues)
we'd love help with.

## Architecture

The game is made up of 4 major components.

1. The web/websocket server (django/django-channels/daphne)

[https://github.com/django/daphne](daphne) is the webserver running django. It's
a pretty standard django application, with the addition of django-channels to
handle websockets. You might note that there are no django models. Originally we
did, but removed them for performance reasons. There is nothing stopping you from
using traditional models with channels.

2. React

We use react to render the game board. React is what we do most of our projects
in, and was a fine choice for local development. In practise, performance isn't
very good because the entire gameboard is re-rendered each tick (5/sec). A future
version will likely use a canvas for rendering.

3. Game Engine (channels/SyncConsumer)

The game engine is also a channels client, but it is a synchronous consumer running
in an infinite loop in its own thread. Actions from the client are published to
a websocket, and a channel layer is used to pass that action to the engine. The
game state is re-rendered on each tick, and then published over a channel layer
back to all the websocket clients.

4. Redis

Redis is the glue between each of the services. Communication between the engine
and the websocket clients is via the redis Channel Layer. Redis will also be used
in the future for maintaining the leaderboards.


# Dev setup

Prerequisites:

- docker >= 17.0
- docker-compose >= 1.8.0
- nodejs >= 7.0
- npm >= 3.10

To setup the development environment, run the setup script:

```
./dev_setup.sh
```

# Running the worker

```bash
$ docker-compose up -d kogame  # start the webserver
$ ./runworker.sh               # run the game engine
```

Now, if you load the site, you will automatically join a new game. Reloading
the page will reconnect you as a new player.
