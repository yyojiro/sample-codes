#!/bin/bash

ALSADEV="plughw:1,0" julius -C grammar-kit/hmm_mono.jconf -input mic -gram mytest -module -nostrip
