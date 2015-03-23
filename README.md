# anki-prompt

Anki-prompt is a little python script
that displays question and answers on
the command line for cards that are due
in the next n days

```
$ anki-prompt.py -h
usage: anki-prompt.py [-h] -d DECK [-s] [--days DAYS]

optional arguments:
  -h, --help            show this help message and exit
  -d DECK, --deck DECK  name of the Anki deck to use
  -s, --show-answer     show the answer in addition to the question
  --days DAYS           number of days to look forward
```

