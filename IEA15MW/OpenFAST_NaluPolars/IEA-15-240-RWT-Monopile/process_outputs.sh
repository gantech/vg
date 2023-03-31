echo -e "Wspeed\tPower" > power_output.txt
echo -e "(m/s)\t(kW)" >> power_output.txt
(echo -en "4.0\t"; sed -n "60009p" output_files/IEA-15-240-RWT_4mps.out | awk '{ print $883 }') >> power_output.txt
(echo -en "5.0\t"; sed -n "60009p" output_files/IEA-15-240-RWT_5mps.out | awk '{ print $883 }') >> power_output.txt
(echo -en "6.0\t"; sed -n "60009p" output_files/IEA-15-240-RWT_6mps.out | awk '{ print $883 }') >> power_output.txt
(echo -en "7.0\t"; sed -n "60009p" output_files/IEA-15-240-RWT_7mps.out | awk '{ print $883 }') >> power_output.txt
(echo -en "8.0\t"; sed -n "60009p" output_files/IEA-15-240-RWT_8mps.out | awk '{ print $883 }') >> power_output.txt
(echo -en "9.0\t"; sed -n "60009p" output_files/IEA-15-240-RWT_9mps.out | awk '{ print $883 }') >> power_output.txt
(echo -en "10.0\t"; sed -n "60009p" output_files/IEA-15-240-RWT_10mps.out | awk '{ print $883 }') >> power_output.txt
(echo -en "11.0\t"; sed -n "60009p" output_files/IEA-15-240-RWT_11mps.out | awk '{ print $883 }') >> power_output.txt
(echo -en "12.0\t"; sed -n "60009p" output_files/IEA-15-240-RWT_12mps.out | awk '{ print $883 }') >> power_output.txt
(echo -en "13.0\t"; sed -n "60009p" output_files/IEA-15-240-RWT_13mps.out | awk '{ print $883 }') >> power_output.txt
(echo -en "14.0\t"; sed -n "60009p" output_files/IEA-15-240-RWT_14mps.out | awk '{ print $883 }') >> power_output.txt
(echo -en "15.0\t"; sed -n "60009p" output_files/IEA-15-240-RWT_15mps.out | awk '{ print $883 }') >> power_output.txt
(echo -en "16.0\t"; sed -n "60009p" output_files/IEA-15-240-RWT_16mps.out | awk '{ print $883 }') >> power_output.txt
(echo -en "17.0\t"; sed -n "60009p" output_files/IEA-15-240-RWT_17mps.out | awk '{ print $883 }') >> power_output.txt
(echo -en "18.0\t"; sed -n "60009p" output_files/IEA-15-240-RWT_18mps.out | awk '{ print $883 }') >> power_output.txt
(echo -en "19.0\t"; sed -n "60009p" output_files/IEA-15-240-RWT_19mps.out | awk '{ print $883 }') >> power_output.txt
(echo -en "20.0\t"; sed -n "60009p" output_files/IEA-15-240-RWT_20mps.out | awk '{ print $883 }') >> power_output.txt
(echo -en "21.0\t"; sed -n "60009p" output_files/IEA-15-240-RWT_21mps.out | awk '{ print $883 }') >> power_output.txt
(echo -en "22.0\t"; sed -n "60009p" output_files/IEA-15-240-RWT_22mps.out | awk '{ print $883 }') >> power_output.txt
(echo -en "23.0\t"; sed -n "60009p" output_files/IEA-15-240-RWT_23mps.out | awk '{ print $883 }') >> power_output.txt
(echo -en "24.0\t"; sed -n "60009p" output_files/IEA-15-240-RWT_24mps.out | awk '{ print $883 }') >> power_output.txt
