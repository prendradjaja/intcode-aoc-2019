#!/usr/bin/env bash

set -ex

python3 -m doctest -v main-02a.py
python3 -m doctest -v main-02b.py
python3 -m doctest -v main-05a.py
python3 -m doctest -v main-05b.py
python3 -m doctest -v main-07a.py
python3 -m doctest -v main-07b.py
python3 -m doctest -v main-09.py

python3 -m doctest -v test-programs.py
