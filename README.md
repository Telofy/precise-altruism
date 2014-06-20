# Precise Altruism

This program contains (will contain) a classification engine for news articles that distinguishes articles that are centrally about topics of charity and altruism from such that have nothing to do with those topics or only touch on them peripherally.

This engine is (will be) used to run a Tumblr or Twitter account that publishes links to these articles based on a broader news feed from Google News or [Kuerzr](http://www.kuerzr.com/).

## Setup

On Ubuntu, the following seems to be necessary:

    sudo aptitude remove python3-numpy  # Just to be sure
    sudo pip3 install numpy

Then just execute the following commands and hope for the best.

    python3 bootstrap.py
    bin/buildout

## Running the Manual Classification

See the usage message with the `--help` option for explanations. Here an example.

    bin/manual_classification -m 0 -f data/altruism.2014-05-13.json link_url content.title content.body

## Generating the Corpora

    bin/corpus_generation data/

## Running the Daemon

TODO

## Running the Tests

    bin/test
