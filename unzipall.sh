#!/bin/bash

find . -name '*.xml.gz' -exec ./unzip.sh '{}' +
