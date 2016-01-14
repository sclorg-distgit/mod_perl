#!/bin/sh

/usr/lib/rpm/perl.prov.stack $* | \
    sed -e '/perl(warnings)/d' \
        -e '/HTTP::Request::Common)/d'

