## LemmyCalBot

A Lemmy bot that creates posts based on calendar events. It reads from a remote calendar, and creates posts in the specified community when every event starts. It gets the title 
and body for the post from the calendar events' title and description respectively.

### Installation

If you have nix, I provide a package: `nix run github:baduhai/lemmycalbot#lemmycalbot`. You can also use this repo as a flake input and install the package to your system.

If you don't have nix (assuming you have python installed):

1. Clone this repo
2. `pip install -r requirements.txt`
3. `chmod +x lemmycalbot.py`

This bot has been tested with Python 3.9. I personally run this bot with a systemd service, passing the PASSWORD environment variable using [LoadCredentialEncrypted=](https://systemd.io/CREDENTIALS/),
but I leave the decision of how to deamonise the bot up to the administrator.

### Usage

```console
usage: lemmycalbot [-h] [-c CALENDAR] [-i INSTANCE] [-u USERNAME] [-p PASSWORD] [-! COMMUNITY]

Calendar based, post-scheduling, Lemmy bot.

optional arguments:
  -h, --help            show this help message and exit
  -c CALENDAR, --calendar CALENDAR
                        Calendar address, make sure to replace webcal:// with https:// or http://
  -i INSTANCE, --instance INSTANCE
                        Instance address, e.g. https://sopuli.xyz
  -u USERNAME, --username USERNAME
                        Bot account username
  -p PASSWORD, --password PASSWORD
                        Bot account password
  -! COMMUNITY, --community COMMUNITY
                        Community name, e.g. indycar

Instead of arguments, environment variables may also be used, set CALENDAR, INSTANCE, USERNAME, PASSWORD and
COMMUNITY. Environment variables take precedence over arguments.
```

If you want an example of this bot in action, look at [!indycar@sopuli.xyz](https://sopuli.xyz/c/indycar) during race weekends! And check out the [indycar](https://github.com/baduhai/lemmycalbot/tree/indycar) 
branch for an explanation and some modifications I've made to the bot to better suit the community's needs.

### Roadmap

- [ ] Add option to pin posts for the duration of the event
- [ ] Add matrix/telegram/email/etc notifications for posts and program failures

### Development

If you have nix, it's as easy as cloning this repo, and running `nix develop`, dependencies are bundled in the devShell. If you don't want to use nix, requirements.txt shows the python libraries used.
