#!/bin/bash

# $1 = uppaal model
# $2 = property in CTL

# -t0 = generate some trace
# -f = prefix Write symbolic traces to files 'prefix-n.xtr' rather than to stderr

echo ../uppaalmac/verifyta -t0 -f $3 $1 $2
verify_output=$({ time ../uppaalmac/verifyta -t0 -f $3 $1 $2; } 2>realtime.txt)
execution_time=`cat realtime.txt`
rm realtime.txt
echo "Time to execute query: $execution_time"
if [[ $verify_output == *"Formula is satisfied."* ]]
	then echo "The property is satisfied"
	echo "$execution_time \t Y \n" >> $4
else
	echo "The property is NOT satisfied"
	echo "Model generated for counterexample"
	echo "$execution_time \t N \n" >> $4
fi
