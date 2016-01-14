#!/bin/sh

/usr/lib/rpm/perl.req.stack $* |\
    sed -e '/perl(Apache2::FunctionTable)/d' \
        -e '/perl(Apache2::StructureTable)/d' \
        -e '/perl(Apache::Test.*)/d' \
	-e '/perl(Data::Flow)/d' \
	-e '/perl(Module::Build)/d' \
    -e '/perl(Apache2::MPM)/d'
