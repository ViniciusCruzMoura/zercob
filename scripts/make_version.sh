#!/bin/sh

#set -xe

YEAR_MONTH=$(git show --no-patch --format=%cd --date=short --date=format:%y.%m $(git rev-parse HEAD))
DATE_COMMITS_BEFORE=$(git show --no-patch --format=%cd --date=short --date=format:%Y-%m-30 $(git rev-parse HEAD))
DATE_COMMITS_AFTER=$(git show --no-patch --format=%cd --date=short --date=format:%Y-%m-01 $(git rev-parse HEAD))
COMMITS=$(git rev-list --count --after="$DATE_COMMITS_AFTER" --before="$DATE_COMMITS_BEFORE" HEAD)
GIT_HASH=$(git rev-parse --short HEAD)

echo v$YEAR_MONTH.$COMMITS-$GIT_HASH
     
