#!/bin/sh

# Show date and time in other time zones

search="$*"

zoneinfo=/usr/share/zoneinfo
format='%a %F %T'

echo "The time in ($search) is:"
find "$zoneinfo" -type f -and -iname "*$search*" -and -not -path "$zoneinfo/right/*" | while read z; do
	d=$(TZ="$z" date +"$format")
	printf "%-24s %23s\n" ${z#$zoneinfo/} "$d"
done
