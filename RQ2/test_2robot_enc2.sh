operatingsystem=1
ktime=100
mapset=("Office.png")
mapidentifier=("j" "p")
xmetersize=("40" "50")
grid=("1")
propnum=5
numeropoi=5
timetestnumber=2
declare -a matrix
#tempi Jupiter
matrix[0,0]=250000
matrix[0,1]=50000
#tempi Poli
matrix[1,0]=400
matrix[1,1]=1200000
resultfile="results.txt"
touch $resultfile

#P1,P2
pointofinterestx1=700
pointofinteresty1=200
pointofinterestx2=500 # non serve
pointofinteresty2=500
#P3
pointofinterestx3=700
pointofinteresty3=350
#P4
pointofinterestx5=700
pointofinteresty5=500

maxgrid=${#grid[@]}
for ((currgridindex=0; currgridindex<${maxgrid}; currgridindex++));
do
		echo "======================================================================================= NEW MODEL.xml CREATED"
	mapindex=$(( $RANDOM % ${#mapset[@]} ))
	currentMap=${mapset[$mapindex]}

	testfile2="Enc2_2robot_M"${mapidentifier[$mapindex]}"_G"$currgridindex".xml"

	echo ../maps/$currentMap
	echo  $testfile
	echo "tipoRobot"
	echo "Span [m]: "${grid[$currgridindex]}
	echo "Side length [m]: "${xmetersize[$mapindex]}

	echo "-----------------------------"
	echo "---- GENERATING THE MAP -----"


    #ENCODING2
	echo "Encoding2 - Model creation"
	python3 ../lib/encoding2xml_2robot.py ../maps/$currentMap  $testfile2 $initposx","$initposy $pointofinterestx1","$pointofinteresty1"@"$pointofinterestx2","$pointofinteresty2"@"$pointofinterestx3","$pointofinteresty3"@"$pointofinterestx5","$pointofinteresty5 "tipoRobot" ${grid[$currgridindex]} ${xmetersize[$mapindex]} $ktime

    for ((prop=0; prop<$propnum; prop++));
        do
        echo "================================================================================ PROPERTY ===="

        echo "(1sec = "$ktime" Uppaal time instant)"

        if [[ "$prop" -eq "0" ]]; then
            propertystring="E<>(P3==1)"
            echo "_______________________________"
            p="E<>(P3==1)"
            echo "Proprietà: "$propertystring
            echo $propertystring > property.q


            testname2="Enc2_2robot_M"${mapidentifier[$mapindex]}"_G"$currgridindex"_TN1_P"$prop
			tracefile2="Enc2_2robot_M"${mapidentifier[$mapindex]}"_G"$currgridindex"_TN1_P"$prop".xtr"

            echo " "
            echo "ENCODING 2"
            gtimeout 600s sh ../uppaalmac/verify.sh  $testfile2 ./property.q   trace/$tracefile2 $resultfile $p $testname2
        fi

        if [[ "$prop" -eq "1" ]]; then
            propertystring="E<>(P4==1)"
            echo "_______________________________"
            p="E<>(P4==1)"
            echo "Proprietà: "$propertystring
            echo $propertystring > property.q


            testname2="Enc2_2robot_M"${mapidentifier[$mapindex]}"_G"$currgridindex"_TN2_P"$prop
			tracefile2="Enc2_2robot_M"${mapidentifier[$mapindex]}"_G"$currgridindex"_TN2_P"$prop".xtr"

            echo " "
            echo "ENCODING 2"
            gtimeout 600s sh ../uppaalmac/verify.sh  $testfile2 ./property.q   trace/$tracefile2 $resultfile $p $testname2
        fi

        if [[ "$prop" -eq "2" ]]; then
            propertystring="E<>(P5==1)"
            echo "_______________________________"
            p="E<>(P5==1)"
            echo "Proprietà: "$propertystring
            echo $propertystring > property.q

            testname2="Enc2_2robot_M"${mapidentifier[$mapindex]}"_G"$currgridindex"_TN3_P"$prop
			tracefile2="Enc2_2robot_M"${mapidentifier[$mapindex]}"_G"$currgridindex"_TN3_P"$prop".xtr"

            echo " "
            echo "ENCODING 2"
            gtimeout 600s sh ../uppaalmac/verify.sh  $testfile2 ./property.q   trace/$tracefile2 $resultfile $p $testname2
        fi

        if [[ "$prop" -eq "3" ]]; then
            propertystring="E<>(P6==1)"
            echo "_______________________________"
            p="E<>(P6==1)"
            echo "Proprietà: "$propertystring
            echo $propertystring > property.q

            testname2="Enc2_2robot_M"${mapidentifier[$mapindex]}"_G"$currgridindex"_TN4_P"$prop
			tracefile2="Enc2_2robot_M"${mapidentifier[$mapindex]}"_G"$currgridindex"_TN4_P"$prop".xtr"

            echo " "
            echo "ENCODING 2"
            gtimeout 600s sh ../uppaalmac/verify.sh  $testfile2 ./property.q   trace/$tracefile2 $resultfile $p $testname2
        fi

        if [[ "$prop" -eq "4" ]]; then
        	for ((timebound=0; timebound<${timetestnumber}; timebound++));
	        do
                proptimeboud=${matrix[$mapindex,$timebound]}

                propertystring="E<>(workcompleted==1 and x<"$proptimeboud")"
                p="E<>(workcompleted==1_and_x<"$proptimeboud")"
                echo "_______________________________"
                echo "Proprietà: "$propertystring
                echo $propertystring > property.q


                testname2="Enc2_2robot_M"${mapidentifier[$mapindex]}"_G"$currgridindex"_T"$timebound"_P"$prop"_task1"
                tracefile2="Enc2_2robot_M"${mapidentifier[$mapindex]}"_G"$currgridindex"_T"$timebound"_P"$prop"_task1.xtr"

                echo " "
                echo "ENCODING 2"
                sh ../uppaalmac/verify.sh  $testfile2 ./property.q   trace/$tracefile2 $resultfile $p $testname2


            done
        fi

	done
done
