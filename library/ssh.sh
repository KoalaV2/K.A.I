#!/bin/bash
ssh=$(last | grep pts/1 | tail -n 1)
sleep 1
echo $ssh
