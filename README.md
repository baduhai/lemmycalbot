## LemmyCalBot

A Lemmy bot that creates threads based on calendar events. It reads from a remote calendar, and creates threads in the specified community when every event starts. It gets the title 
and body for the thread from the calendar events' title and description respectively.

### Usage

```console
usage: LemmyCalBot [-h] [-c CALENDAR] [-i INSTANCE] [-u USERNAME] [-p PASSWORD] [-! COMMUNITY]

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

- [ ] Add option to pin and unpin threads for the duration of the event
