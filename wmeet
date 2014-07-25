#!/bin/zsh

zoneinfo=/usr/share/zoneinfo

refoff='GMT-4:00'
reftz='EST5EDT'

refdt="$(date "+%a %F")"
refhr="$(TZ="$ltz" date "+%H")"
refmin="$(TZ="$ltz" date "+%M")"

tzs=()
for tz in $*; do
	tzs+="${$(find "$zoneinfo" -type f -and -iname "*$tz*" -and -not -path "$zoneinfo/right/*" | head -n1)#$zoneinfo/}"
done

datefmt='%a %d-%b'
timefmt='%H:%M'

printf " %16s" "-"
for tz in $tzs; do
	printf "  %16s" "$tz"
done
printf "\n"

for hr in $(seq 0 23); do
	ref="$refdt $hr:$refmin $refoff"

	state="$(TZ="$reftz" date "+$datefmt" -d "$ref")"
	if [[ "$refst" == "$state" ]]; then
		reffmt="$timefmt"
	else
		reffmt="$datefmt $timefmt"
	fi
	refst="$state"
	reftime="$(TZ="$reftz" date "+$reffmt" -d "$ref")"
	
	if [[ $hr == $refhr ]]; then printf "*"; else printf " "; fi
	printf "%16s" "$reftime"

	i=1
	for tz in $tzs; do
		state="$(TZ="$tz" date "+$datefmt" -d "$ref")" 
		if [[ "$tzstate[$i]" == "$state" ]]; then
			tzfmt="$timefmt"
		else
			tzfmt="$datefmt $timefmt"
		fi
		tzstate[$i]="$state"
		tztime=$(TZ="$tz" date "+$tzfmt" -d "$ref")
		i=$((i+1))

		printf "  %16s" "$tztime"
	done
	printf "\n"

done
