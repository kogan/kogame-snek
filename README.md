# Kogame

Kogame - pronounced with 3 syllables - is a Django Channels real-time or turn-based game platform


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

# TODO

- Custom usernames and Join/Rejoin button, rather than autojoin
- Death messages
- Send errors back to client (can't join, too full, etc)
- Leaderboards (store ticks + length per user in redis)
- Prevent username collisions (auth?)
- Current players in game
- Distinguish between current player and other players
- Better snake icons/tiles
