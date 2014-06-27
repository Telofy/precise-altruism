# Precise Altruism

This program contains (will contain) a classification engine for news articles that distinguishes articles that are centrally about topics of charity and altruism from such that have nothing to do with those topics or only touch on them peripherally.

This engine is (will be) used to run a Tumblr or Twitter account that publishes links to these articles based on a broader news feed from Google News or [Kuerzr](http://www.kuerzr.com/).

## Setup

Precise Altruism might work with Python 3, but 2.7 should be safer at this point.

On Ubuntu, the following seems to be necessary when using Python 3:

    sudo aptitude remove python3-numpy  # Just to be sure
    sudo pip3 install numpy

You may also have to install some packages globally:

    sudo aptitude install python-numpy python-scipy libzmq-dev g++

Then just execute the following commands and hope for the best.

    python2.7 bootstrap.py
    bin/buildout

You may have to run `bin/buildout` twice if it can’t download the NLTK data on the first run when `bin/python` does not yet exist.

## Running the Manual Classification

See the usage message with the `--help` option for explanations. Here an example.

    bin/manual_classification -m 0 -f data/altruism.2014-05-13.json link_url content.title content.body

## Generating the Corpora

    bin/corpus_generation data/

## Running the Evaluation

    bin/evaluation

## Running the Daemon

    bin/daemon

## Running the Tests

    bin/test
