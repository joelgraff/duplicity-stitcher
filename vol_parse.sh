#!/bin/bash

for name in *vol12?.difftar.gz; do

	prefix=${name%%vol*}
	infix=${name#"$prefix"}
	infix=${infix%.difftar.gz}

	gzip -dc < $name > $infix

	echo $infix

done
