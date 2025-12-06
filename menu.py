#! /usr/bin/env python3
# sam. 06 déc. 2025 17:21:04 CET <christophe@pallier.org>

import npyscreen
import os
import sys
import datetime
import subprocess

# --- Persistence Configuration ---
SUBJECT_FILE = ".last_subject.txt"

# --- Load Previous Subject ID if exists ---
default_subject = "1"
if os.path.exists(SUBJECT_FILE):
    try:
        with open(SUBJECT_FILE, 'r') as f:
            content = f.read().strip()
            if content:
                default_subject = content
    except IOError:
        pass # If file is unreadable, ignore it

# --- Configuration & Environment Defaults ---
os.environ['SUBJECT'] = os.environ.get('SUBJECT', '1')
os.environ['EXPYRIMENT_DISPLAY'] = os.environ.get('EXPYRIMENT_DISPLAY', '0')
os.environ['EXPYRIMENT_DISPLAY_RESOLUTION'] = os.environ.get('EXPYRIMENT_DISPLAY_RESOLUTION', '1920x1080')

CMD_LOCALIZER_BASE = (
    "python pinel_localizer.py --background-color 0 0 0 "
    "--text-color 250 250 250 --rsvp-display-time 250 "
    "--rsvp-display-isi 100 --picture-display-time 200 "
    "--picture-isi 0 --fs_delay_time 100 "
    "--stim-dir stim_files --total-duration 305000"
)

class PinelLocalizerApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", MainMenu, name="Pinel Localizer")

class MainMenu(npyscreen.FormBaseNew):
    def create(self):
        # 1. Info Header
        self.status_text = self.add(
            npyscreen.FixedText, 
            value=self.get_header_text(), 
            editable=False,
            color='GOOD'
        )
        
        self.add(npyscreen.FixedText, value=" ", editable=False) # Spacer

        # 2. Direct Subject Input Widget
        # "TitleText" allows the user to type directly.
        self.subject_widget = self.add(
            npyscreen.TitleText, 
            name="Subject ID:", 
            value=os.environ['SUBJECT'],
            begin_entry_at=14  # Align text slightly
        )

        self.add(npyscreen.FixedText, value=" ", editable=False) # Spacer

        # 3. The Action Menu
        # Note: "Edit Subject" is removed from this list
        self.menu = self.add(
            MainMenuOptionList, 
            name="Select Action (TAB to switch between Subject ID and Menu)", 
            values=[
                "1. Effectuer un calibrage",
                "2. Afficher les instructions",
                "3. Run 1",
                "4. Run 2",
                "5. Run 3",
                "6. Run 4",
                "Quit"
            ],
            scroll_exit=True
        )

    def get_header_text(self):
        return (f"Time={datetime.datetime.now().strftime("%H:%M:%S")} | "
                f"SCREEN={os.environ['EXPYRIMENT_DISPLAY']} | "
                f"RES={os.environ['EXPYRIMENT_DISPLAY_RESOLUTION']}")

    def beforeEditing(self):
        # Update header just before drawing
        self.status_text.value = self.get_header_text()

class MainMenuOptionList(npyscreen.MultiLineAction):
    def actionHighlighted(self, act_on_this, key_press):
        selection = act_on_this.split(".")[0] if "." in act_on_this else act_on_this
        
        # --- CRITICAL STEP ---
        # Before running ANY command, grab the Subject ID currently typed 
        # in the widget above and update the environment variable.
        current_subject_input = self.parent.subject_widget.value
        os.environ['SUBJECT'] = str(current_subject_input)
        
        # Update the header text to match (for visual confirmation)
        self.parent.status_text.value = self.parent.get_header_text()
        self.parent.status_text.display()

        # 3. Save to File (Persistence)
        try:
            with open(SUBJECT_FILE, 'w') as f:
                f.write(current_subject_input)
        except IOError:
            # If we can't save the file (permissions?), just ignore it to not crash the run
            pass

        # 4. Execute Action
        if "Quit" in act_on_this:
            self.parent.parentApp.switchForm(None)
        else:
            self.run_experiment(selection)

    def run_experiment(self, selection_index):
        cmd_suffix = ""
        desc = ""
        
        # Adjusted indices because "Edit Subject" was removed
        if selection_index == "1":
            desc = "Calibration"
            cmd_suffix = " --cali 1"
        elif selection_index == "2":
            desc = "Instructions"
            cmd_suffix = " --splash instructions_localizer.csv"
        elif selection_index == "3":
            desc = "Session 1"
            cmd_suffix = " --csv_file run1_pinel_localizer.csv"
        elif selection_index == "4":
            desc = "Session 2"
            cmd_suffix = " --csv_file run2_pinel_localizer.csv"
        elif selection_index == "5":
            desc = "Session 3"
            cmd_suffix = " --csv_file run3_pinel_localizer.csv"
        elif selection_index == "6":
            desc = "Session 4"
            cmd_suffix = " --csv_file run4_pinel_localizer.csv"

        if cmd_suffix:
            full_command = CMD_LOCALIZER_BASE + cmd_suffix
            
            npyscreen.blank_terminal()
            print(full_command)
            try:
                subprocess.call(full_command, shell=True)
            except KeyboardInterrupt:
                pass
            #input("\nPress Enter to return to menu...")
            self.parent.curses_pad.clear()

            # Auto-increment logic
            # Run 1 is now at index 2 in the list (0:Cali, 1:Instr, 2:Run1)
            current_index = self.cursor_line
            
            # If current is Run 1 (index 2) to Run 3 (index 4), move down
            if 2 <= current_index < 5:
                self.cursor_line += 1
            elif current_index == 5: # If Run 4, move to Quit
                self.cursor_line += 1
            
            self.parent.display()

if __name__ == "__main__":
    try:
        app = PinelLocalizerApp()
        app.run()
    except KeyboardInterrupt:
        sys.exit(0)
