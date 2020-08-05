#!/usr/bin/env bash

vue-cli-service build

rm ../static/js/app.*.js
rm ../static/js/app.*.js.map

cd build/
mv index.html ../../templates/vue/

cd static/js/
mv * ../../../../static/js/

cd ../../../
rm -r build/