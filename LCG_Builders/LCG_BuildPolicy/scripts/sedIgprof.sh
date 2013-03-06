#!/bin/bash

if [ -e $1/sedDoneForIgprof ]; then
	echo "These files have been already altered for ifprof execution. Exiting..."
	exit
fi

touch $1/sedDoneForIgprof

for i in `find "$1" -name '*.qmt'`; do
	filename=$(basename "$i" .qmt)
	path=$(dirname "$i")
	previous=$(basename $path)
	p_extension=${previous##*.}
	p_filename=${previous%.*}
	while [ x"${p_extension}" == "xqms" ]; do
		filename=${p_filename}.${filename}
		path=$(dirname $path)
		previous=$(basename $path)
		p_extension=${previous##*.}
		p_filename=${previous%.*}
	done
	sed -n '
	  # if the first line copy the pattern to the hold buffer
	  1h
	  # if not the first line then append the pattern to the hold buffer
	  1!H
	  # if the last line then ...
	  $ {
	  	# copy from the hold to the pattern buffer
		g
		# do the search and replace
		s/name="\(command\|program\)"\s*>\s*<text>\s*\([^<]*\)<\/text>/name="\1"><text>runIgprof.sh '${filename}' "\2"<\/text>/g
		s/name="stdout"\s*>\s*<text>[^<]*<\/text>/name="stdout"><text\/>/g
		s/<argument name="stdout_ref"\s*>\([^<]\|<\/\?text>\)*<\/argument>//g
		s/<argument name="stdout_ref_path"\s*>\([^<]\|<.\?text>\)*<\/argument>//g
		s/name="stderr"\s*>\s*<text>[^<]*<\/text>/name="stderr"><text\/>/g
		s/<argument name="stderr_ref"\s*>\([^<]\|<.\?text>\)*<\/argument>//g
		s/<argument name="stderr_ref_path"\s*>\([^<]\|<.\?text>\)*<\/argument>//g
		# print
		p
	}' "$i" > "$i".igf.tmp
	mv -f "$i".igf.tmp "$i"
done
echo "QMT files altered to execute tests with igprof"
