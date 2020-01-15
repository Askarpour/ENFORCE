#!/bin/bash

# $1 = uppaal model
# $2 = property in CTL
# $3 = trace file
# $4 = results.txt
# $5 = property
# $6 = nome test

# -t0 = generate some trace
# -f = prefix Write symbolic traces to files 'prefix-n.xtr' rather than to stderr
#echo $1
#echo $2 
#echo $3
#echo $4


#echo "./uppaalLinux/verifyta -t0 -f $3 $1 $2;"

../uppaalLinux/verifyta -t0 -f $3 $1 $2



verify_output=$({ time ../uppaalLinux/verifyta -t0 -f $3 $1 $2; } 2>realtime.txt)
{time ../uppaalLinux/verifyta -t0 -f $3 $1 $2 ; } 2>time.txt
#{time sleep 1 2>time.txt;}

execution_time=`cat realtime.txt`

#


LIST=$verify_output
SOURCE="Formula is NOT satisfied"
if echo "$LIST" | grep -q "$SOURCE"; then
	#tempo=$(echo $execution_time | cut -c1-55)
    tempo=$(echo $execution_time)
	echo $6"\t  NO   \t Uppaal time: "$tempo"\t Property: "$5 >> $4

else
	#tempo=$(echo $execution_time | cut -c60-118)
    tempo=$(echo $execution_time)
	echo $6"\t  YES  \t Uppaal time:"$tempo"\t Property: "$5 >> $4
fi

#echo "$---------------------------------------------------------------------------\t  \n" >> $4
echo "$  \n" >> $4






#if [[ $verify_output == *"Formula is satisfied."* ]]
#	then echo "The property is satisfied"
#	echo "$execution_time \t Y \n" >> $4
#else
#	echo "The property is NOT satisfied"
#	#echo "Model generated for counterexample"
#	echo "$execution_time \t N \n" >> $4
#fi
