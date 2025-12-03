#! /bin/bash



tempfile=`(tempfile) 2>/dev/null` || tempfile=/tmp/test$$
trap "rm -f $tempfile" 0 $SIG_NONE $SIG_HUP $SIG_INT $SIG_QUIT $SIG_TERM

resp=0

cmd_localizer='python localizer_standard.py --background-color 0 0 0 
            --text-color 250 250 250 --rsvp-display-time 250 
            --rsvp-display-isi 100 --picture-display-time 200 
            --picture-isi 0 --fs_delay_time 100 
            --stim-dir stim_files --total-duration 305000'


until [ "$resp" = "Quit" ]
do
    next=$(($resp + 1))
    if [ $next = "11" ]; then
        next="Quit";
    fi

    dialog --clear --title "Localizer standard" "$@" \
         --nocancel --default-item  "$next" \
         --menu "Sélectionner votre choix et appuyer sur entrée\n" \
             24 40 7 \
             1 "Effectuer un calibrage" \
             2 "Afficher les instructions" \
             3 "Run 1 " \
             4 "Run 2" \
             5 "Run 3" \
             6 "Run 4" \
             Quit  "End the experiment"  2>$tempfile

  retvat=$?
  resp=$(cat $tempfile)

  case $resp in
      1) cali=' --cali 1'
         echo "calibration"
	 echo $cmd_localizer$cali
         $cmd_localizer$cali;;
      2) instructions=' --splash instructions_localizer.csv'
         echo "instructions"
         $cmd_localizer$instructions;;
      3) session=' --csv_file session1_localizer_standard.csv'
         echo "session 1"
         echo $cmd_localizer$session
         $cmd_localizer$session;;
      4) session=' --csv_file session2_localizer_standard.csv'
         echo "session 2"
         echo $cmd_localizer$session
         $cmd_localizer$session;;
      5) session=' --csv_file session3_localizer_standard.csv'
         echo "session 3"
         echo $cmd_localizer$session
         $cmd_localizer$session;;
      6) session=' --csv_file session4_localizer_standard.csv'
         echo "session 4"
         echo $cmd_localizer$session
         $cmd_localizer$session;;
      Quit) echo "Finito!" ;;
      *) dialog --msgbox "I do not understand..." 6 32 ;;
  esac

done
