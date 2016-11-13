#!/bin/bash

${CC:-clang} -shared -Wl,-install_name,libfuzzy.so -o libfuzzy.so -fPIC fuzzy.c
