#!/bin/bash

command -v python &>/dev/null || { echo "python not found"; exit 1; }

version=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if [[ $version != "2.7" ]]; then
	echo "your python is version $version, but we need 2.7"
	exit 1
fi

pip install python-dateutil amadeus nltk simplejson spacy && echo "SUCCESS"
