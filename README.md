# Precise Altruism

This program contains (will contain) a classification engine for news articles that distinguishes articles that are centrally about topics of charity and altruism from such that have nothing to do with those topics or only touch on them peripherally.

This engine is (will be) used to run a Tumblr or Twitter account that publishes links to these articles based on a broader news feed from Google News or [Kuerzr](http://www.kuerzr.com/).

## Target Audience

Our envisioned reader is interested in topics that maximize the following in roughly that order:

    1. Altruism
    2. Effectiveness
    3. Timeless relevance

## Setup

You may have to install some packages globally:

    sudo aptitude install python-numpy python-scipy libzmq-dev g++

Then just execute the following commands and hope for the best.

    python2.7 bootstrap.py
    bin/buildout

You may have to run `bin/buildout` twice if it can’t download the NLTK data on the first run when `bin/python` does not yet exist, but theoretically that shouldn’t happen.

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
