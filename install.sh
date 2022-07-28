#!/bin/bash

cp launcher.template GCoder.desktop

pwd=$(pwd)

sed -i "s|PATH|$pwd|g" GCoder.desktop

chmod u+x ./GCoder.desktop
