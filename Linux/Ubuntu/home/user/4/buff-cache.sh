#!/bin/bash

free
echo ------------------
dd if=/dev/zero of=testfile bs=1M count=1K
echo ------------------
free
echo ------------------
rm testfile
echo ------------------
free