#!/bin/bash

git checkout $(git log --reverse | head -n 1 | sed -e "s/commit\ //g") && git branch -D master && git checkout master && git pull
