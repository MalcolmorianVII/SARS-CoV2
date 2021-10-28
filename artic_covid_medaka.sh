#! /usr/bin/bash
# $1 to denote which subcommand to run
# For guppyplex the argv means:
	# $2 {min}
	# $3 {max}
	# $4 {input}
	# $5 {batch_name}
	# $6 {ouput} .... guppyplex

# For minion argv means:
	# $2 {input.p_schemes} ....minion
	# $3 {scheme}
	# $4 {medaka_model}
	# $5 {input.gu}
	# $6 {output} .... minion
set -e
eval "$(conda shell.bash hook)"
conda activate "artic"

if [ $1 == "guppyplex" ]
then
	artic guppyplex --min-length $2 --max-length $3 --directory $4 --prefix $5 --out $6
elif [ $1 == "minion" ]
then
	artic minion --medaka --scheme-directory $2/$3 --medaka-model $4 --normalise 200 --threads 4 --read-file $5 $3 $6
else
	echo "Invalid subcommand....Terminating pipeline now"
fi

exit 0