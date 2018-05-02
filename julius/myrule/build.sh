#!/bin/bash -eu

BASENAME=$@

if [ -z "$BASENAME" ]
then
    echo "usage: $0 BASENAME" >&2
    exit 1
fi

iconv -f utf8 -t eucjp $BASENAME.yomi | perl grammar-kit/bin/linux/yomi2voca.pl | iconv -f eucjp -t utf8 > $BASENAME.voca
mkdfa.pl $BASENAME
generate $BASENAME
