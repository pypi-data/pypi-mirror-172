# timetable-cli
## How to use
```
Usage: timetable-cli [OPTIONS] COMMAND [ARGS]...

Options:
  --config TEXT                  [required]
  --db TEXT                      [required]
  --debug
  -d, --global-timedelta TEXT
  --list-categories
  -c, --columns TEXT
  --table-kwargs TEXT
  --ignore-time-status
  --combine-title-and-variation
  --help                         Show this message and exit.

Commands:
  show
  status
  watch
```
```
Usage: timetable-cli show [OPTIONS] [SELECTORS]...

Options:
  --help  Show this message and exit.
```
```
Usage: timetable-cli watch [OPTIONS]

Options:
  --text TEXT
  --interval INTEGER
  --notification
  --notification-cmd TEXT
  --voice
  --voice-cmd TEXT
  --notify-eta TEXT
  --table-selectors TEXT
  --help                   Show this message and exit.
```
```
Usage: timetable-cli status [OPTIONS]

Options:
  --help  Show this message and exit.
```
