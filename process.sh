#!/bin/bash
WRKDIR="src/profiles.d"
cd $WRKDIR

function write_file ()
{
	filename="$1"
	cp "$filename" "${filename}.bk"
	echo -n > "$filename"
	echo $filename

}
while read -r; do
	FIRSTCHAR=${REPLY:0:1}
	if [[ "x$FIRSTCHAR" != "x " ]]
	then
		if [[ "x$FIRSTCHAR" != "x}" ]] && [[ "x$FIRSTCHAR" != "x" ]] && [[ "x$FIRSTCHAR" != "x#" ]]
		then
			filename=${REPLY/profile /}
			filename=$(basename ${filename/ */})
    		write_file "$filename"
		elif [[ "x$FIRSTCHAR" == "x}" ]]
		then
			echo "$REPLY">>"$filename"
			continue
		elif [[ "x$FIRSTCHAR" == "x#" ]]
		then
			continue
		fi
	fi
	echo "$REPLY" >> "$filename"
done < /etc/apparmor.d/security.profile
