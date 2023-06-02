#!/bin/bash
pip install --upgrade pip
pip install -r ../../requirements-dev.txt
pip install $DKU_DSS_URL/public/packages/dataiku-internal-client.tar.gz