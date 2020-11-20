#!/bin/sh
git add build && git commit -m "Add new build" && git push && git subtree push --prefix build origin gh-pages