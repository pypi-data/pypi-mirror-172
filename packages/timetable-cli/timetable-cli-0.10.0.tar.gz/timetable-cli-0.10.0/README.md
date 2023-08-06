# timetable-cli
## How to use
```
Usage: timetable-cli [OPTIONS] [ACTIVITIES_SELECTOR]...

Options:
  --config TEXT                  Config module
  --db TEXT                      Database file.
  --debug                        Show debug info.
  --add-empty-lines
  -d, --global-timedelta TEXT
  -D, --show-date                Show current date and time.
  -S, --show-status              Show info about current and next activities.
  -A, --show-activities          Show activities table filtered by
                                 activities_selectors.
  --list-categories              Show activities categories when rendering
                                 activities table.
  -c, --columns TEXT             Columns to display when rendering activities
                                 table.
  --table-kwargs TEXT            Activities table kwargs (json)
  --ignore-time-status
  --combine-title-and-variation  Append activity variation to title when
                                 rendering activities table.
  -R, --show-rules               Show random rule.
  -r, --rules-list               Show rules table instead of random rule.
  -Q, --show-quotes              Show random quote.
  -q, --quotes-list              Show quotes table instead of random quote.
  -W, --watch
  --watch-text TEXT
  --watch-interval INTEGER
  --watch-clear-screen
  --watch-notification
  --watch-notification-cmd TEXT
  --watch-voice
  --watch-voice-cmd TEXT
  --watch-notify-eta TEXT
  --help                         Show this message and exit.
```
