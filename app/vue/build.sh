#!/usr/bin/env bash

vue-cli-service build
cd build/
mv index.html ../../templates/vue/

cd static/js/
mv * ../../../../static/js/

cd ../../../
rm -r build/