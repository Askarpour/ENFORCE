operatingsystem=1
ktime=100
mapset=("JupiterImg.png")
 # "Edificio20.PNG" "Edificio22.PNG")
mapidentifier=("j" "p")
xmetersize=("80" "50")
grid=("1.3" "1" "0.8" "0.6" "0.4")
# grid=("0.25" "0.5" "1")
propnum=3
numeropoi=3
timetestnumber=2
declare -a matrix
#tempi Jupiter
matrix[0,0]=6000
matrix[0,1]=2300000
#tempi Poli
matrix[1,0]=4000
matrix[1,1]=1200000
#tempi Poli
matrix[2,0]=4000
matrix[2,1]=1200000

resultfile="results.txt"
touch $resultfile

initposx=135
initposy=170

pointofinterestx1=$initposx
pointofinteresty1=$initposy
pointofinterestx2=490
pointofinteresty2=160
pointofinterestx3=470
pointofinteresty3=250

maxgrid=${#grid[@]}
for ((currgridindex=0; currgridindex<${maxgrid}; currgridindex++));
do
	echo "======================================================================================= NEW MODEL.xml CREATED"
	mapindex=$(( $RANDOM % ${#mapset[@]} ))
	currentMap=${mapset[$mapindex]}

	testfile1="Enc1_M"${mapidentifier[$mapindex]}"_G"$currgridindex".xml"
	testfile2="Enc2_M"${mapidentifier[$mapindex]}"_G"$currgridindex".xml"

	echo  ../maps/$currentMap
	echo  $testfile
	echo "tipoRobot"
	echo "Span [m]: "${grid[$currgridindex]}
	echo "Side length [m]: "${xmetersize[$mapindex]}

	echo "-----------------------------"
	echo "---- GENERATING THE MAP -----"

  #ENCODING1
	echo "Encoding1 - Model creation"
	python3 ../lib/encoding1xml.py  ../maps/$currentMap  $testfile1 $initposx","$initposy $pointofinterestx1","$pointofinteresty1"@"$pointofinterestx2","$pointofinteresty2"@"$pointofinterestx3","$pointofinteresty3 "tipoRobot" ${grid[$currgridindex]} ${xmetersize[$mapindex]} $ktime
	echo "Encoding2 - Model creation"
	python3 ../lib/encoding2xml.py  ../maps/$currentMap  $testfile2 $initposx","$initposy $pointofinterestx1","$pointofinteresty1"@"$pointofinterestx2","$pointofinteresty2"@"$pointofinterestx3","$pointofinteresty3 "tipoRobot" ${grid[$currgridindex]} ${xmetersize[$mapindex]} $ktime

  for ((prop=0; prop<$propnum; prop++));
      do
      echo "================================================================================ PROPERTY ===="
      echo "(1sec = "$ktime" Uppaal time instant)"
      if [[ "$prop" -eq "0" ]]; then
          propertystring="E<>(P2==1)"
          echo "_______________________________"
          p="E<>(P2==1)"
          echo "Proprietà: "$propertystring
          echo $propertystring > property.q

          testname1="Enc1_M"${mapidentifier[$mapindex]}"_G"$currgridindex"_TN1_P"$prop
          tracefile1="Enc1_M"${mapidentifier[$mapindex]}"_G"$currgridindex"_TN1_P"$prop".xtr"
          testname2="Enc2_M"${mapidentifier[$mapindex]}"_G"$currgridindex"_TN1_P"$prop
					tracefile2="Enc2_M"${mapidentifier[$mapindex]}"_G"$currgridindex"_TN1_P"$prop".xtr"

          echo " "
          echo "ENCODING 1"
          ../uppaalLinux/verify.sh  $testfile1 ./property.q   trace/$tracefile1 $resultfile $p $testname1
          echo " "
          echo "ENCODING 2"
          timeout 600s ../uppaalLinux/verify.sh  $testfile2 ./property.q   trace/$tracefile2 $resultfile $p $testname2
      fi
      if [[ "$prop" -eq "1" ]]; then
          propertystring="E<>(P3==1)"
          echo "_______________________________"
          p="E<>(P3==1)"
          echo "Proprietà: "$propertystring
          echo $propertystring > property.q

          testname1="Enc1_M"${mapidentifier[$mapindex]}"_G"$currgridindex"_TN2_P"$prop
          tracefile1="Enc1_M"${mapidentifier[$mapindex]}"_G"$currgridindex"_TN2_P"$prop".xtr"
          testname2="Enc2_M"${mapidentifier[$mapindex]}"_G"$currgridindex"_TN2_P"$prop
					tracefile2="Enc2_M"${mapidentifier[$mapindex]}"_G"$currgridindex"_TN2_P"$prop".xtr"

          echo " "
          echo "ENCODING 1"
          ../uppaalLinux/verify.sh  $testfile1 ./property.q   trace/$tracefile1 $resultfile $p $testname1
          echo " "
          echo "ENCODING 2"
          timeout 600s ../uppaalLinux/verify.sh  $testfile2 ./property.q   trace/$tracefile2 $resultfile $p $testname2
      fi
      if [[ "$prop" -eq "2" ]]; then
      	for ((timebound=0; timebound<${timetestnumber}; timebound++));
        do
              proptimeboud=${matrix[$mapindex,$timebound]}
              propertystring="E<>(P1==1 and workcompleted==1 and x<"$proptimeboud")"
              p="E<>(P1==1_and_workcompleted==1_and_x<"$proptimeboud")"
              echo "_______________________________"
              echo "Proprietà: "$propertystring
              echo $propertystring > property.q

              testname1="Enc1_M"${mapidentifier[$mapindex]}"_G"$currgridindex"_T"$timebound"_P"$prop
		    			tracefile1="Enc1_M"${mapidentifier[$mapindex]}"_G"$currgridindex"_T"$timebound"_P"$prop".xtr"
              testname2="Enc2_M"${mapidentifier[$mapindex]}"_G"$currgridindex"_T"$timebound"_P"$prop
              tracefile2="Enc2_M"${mapidentifier[$mapindex]}"_G"$currgridindex"_T"$timebound"_P"$prop".xtr"

              echo " "
              echo "ENCODING 1"
              ../uppaalLinux/verify.sh  $testfile1 ./property.q   trace/$tracefile1 $resultfile $p $testname1
              echo " "
              echo "ENCODING 2"
              timeout 600s ../uppaalLinux/verify.sh  $testfile2 ./property.q   trace/$tracefile2 $resultfile $p $testname2
          done
      fi
	done
done
