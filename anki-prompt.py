#!/usr/bin/env python

import sys
from os.path import expanduser
import os
sys.path.append(os.path.join(expanduser("~"), "src/anki"))

from anki import Collection
from sqlite3 import OperationalError
from termcolor import colored
from argparse import ArgumentParser

import re
import random
import sys

parser = ArgumentParser()
parser.add_argument('-c', '--collection', required=True,
                    help='path to the anki database')
parser.add_argument('-d', '--deck', required=True,
                    help='name of the Anki deck to use')
parser.add_argument('-s', '--show-answer', action='store_true',
                    help='show the answer in addition to the question')
parser.add_argument('--days', required=False,
                    default=1,
                    help='number of days to look forward')


args = parser.parse_args()

try:
    col = Collection(args.collection)
except OperationalError:
    print(colored("Anki Deck locked", "magenta"))
    sys.exit(0)
except Exception as e:
    print(colored("Error loading collection", "magenta"))
    sys.exit(0)

deck = col.decks.byName(args.deck)

if not deck:
    print(colored("Deck {} not found".format(args.deck), "magenta"))
    sys.exit(0)

cards = col.db.list(
    "select id from cards where did={} and due between {} and {}".format(
        deck['id'], col.sched.today, col.sched.today + int(args.days)))

qas = col.renderQA(cards)
qa = random.choice(qas)

question = qa['q'].encode('utf-8')
answer = qa['a'].encode('utf-8')
question = re.sub('\[\[.*?\]\]', '', question)
answer = re.sub('.*answer>', '', answer, flags=re.DOTALL)

print(colored(question.strip(), "yellow", attrs=['dark'])),

if args.show_answer:
    print(colored(answer.strip(), "grey", attrs=['dark']))

with open(os.path.join(expanduser("~"), ".anki-answer"), "wb") as f:
        f.write(answer.strip())
