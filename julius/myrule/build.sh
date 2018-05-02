#!/bin/bash

iconv -f utf8 -t eucjp mytest.yomi | perl grammar-kit/bin/linux/yomi2voca.pl | iconv -f eucjp -t utf8 > mytest.voca
mkdfa.pl mytest
generate mytest
