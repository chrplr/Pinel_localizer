#! /bin/bash
# <christophe@Pallier.org> sam. 06 déc. 2025 10:17:11 CET


export SUBJECT=${SUBJECT:-1}
export EXPYRIMENT_DISPLAY=${EXPYRIMENT_DISPLAY:-0}
export EXPYRIMENT_DISPLAY_RESOLUTION=${EXPYRIMENT_DISPLAY_RESOLUTION:-"1920x1080"}

# Create a temporary file to store dialog's output
# mktemp creates a safe, unique temporary file
OUTPUT_FILE=$(mktemp)
# Function to ensure we clean up the temp file on exit (even if crashed)
trap "rm -f $OUTPUT_FILE" EXIT

tempfile=`(tempfile) 2>/dev/null` || tempfile=/tmp/test$$
trap "rm -f $tempfile" 0 $SIG_NONE $SIG_HUP $SIG_INT $SIG_QUIT $SIG_TERM

resp=0

cmd_localizer='python pinel_localizer.py --background-color 0 0 0 
            --text-color 250 250 250 --rsvp-display-time 250 
            --rsvp-display-isi 100 --picture-display-time 200 
            --picture-isi 0 --fs_delay_time 100 
            --stim-dir stim_files --total-duration 305000'


until [ "$resp" = "Quit" ]
do
    next=$(($resp + 1))
    if [ $next = "7" ]; then
        next="Quit";
    fi

    dialog --clear --title "Pinel Localizer" "$@" \
         --nocancel --default-item  "$next" \
         --menu "subject=$SUBJECT; screen=$EXPYRIMENT_DISPLAY; RES=$EXPYRIMENT_DISPLAY_RESOLUTION\n" \
             24 40 7 \
	     1 "Edit Subject number" \
             2 "Effectuer un calibrage" \
             3 "Afficher les instructions" \
             4 "Run 1 " \
             5 "Run 2" \
             6 "Run 3" \
             7 "Run 4" \
             Quit  "End the experiment"  2>$tempfile

  retvat=$?
  resp=$(cat $tempfile)

  echo "$resp"
  sleep 1
  case $resp in
      1) 
            # We pre-fill the box with $SUBJECT so the user can edit it
            dialog --title "Edit Configuration" \
            --inputbox "Enter SUBJECT id:" 8 60 "$SUBJECT" 2> "$OUTPUT_FILE"

            # Check if user hit OK
            if [ $? -eq 0 ]; then
                # Update the variable
                NEW_VALUE=$(cat "$OUTPUT_FILE")
                
                # Basic validation (optional)
                if [[ -z "$NEW_VALUE" ]]; then
                    dialog --msgbox "Error: Value cannot be empty!" 6 40
                else
                    SUBJECT="$NEW_VALUE"
                    dialog --msgbox "Success! Value updated." 6 40
                fi
            else
                dialog --msgbox "Change cancelled." 5 30
            fi
            ;;
      2) cali=' --cali 1'
         echo "calibration"
	 echo $cmd_localizer$cali
         $cmd_localizer$cali;;
      3) instructions=' --splash instructions_localizer.csv'
         echo "instructions"
         $cmd_localizer$instructions;;
      4) session=' --csv_file session1_localizer_standard.csv'
         echo "session 1"
         echo $cmd_localizer$session
         $cmd_localizer$session;;
      5) session=' --csv_file session2_localizer_standard.csv'
         echo "session 2"
         echo $cmd_localizer$session
         $cmd_localizer$session;;
      6) session=' --csv_file session3_localizer_standard.csv'
         echo "session 3"
         echo $cmd_localizer$session
         $cmd_localizer$session;;
      7) session=' --csv_file session4_localizer_standard.csv'
         echo "session 4"
         echo $cmd_localizer$session
         $cmd_localizer$session;;
      Quit) ;;
      *) dialog --msgbox "$RESP not in the menu" 6 32 ;;
  esac

done
