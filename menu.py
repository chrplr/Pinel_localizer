import npyscreen
import os
import sys
import subprocess

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
        # Header displaying current config
        self.status_text = self.add(
            npyscreen.FixedText, 
            value=self.get_header_text(), 
            editable=False,
            color='GOOD'
        )
        
        self.add(npyscreen.FixedText, value=" ", editable=False) # Spacer

        self.menu = self.add(
            MainMenuOptionList, 
            name="Selection", 
            values=[
                "1. Edit Subject number",
                "2. Effectuer un calibrage",
                "3. Afficher les instructions",
                "4. Run 1",
                "5. Run 2",
                "6. Run 3",
                "7. Run 4",
                "Quit"
            ],
            scroll_exit=True
        )

    def get_header_text(self):
        return (f"subject={os.environ['SUBJECT']}; "
                f"screen={os.environ['EXPYRIMENT_DISPLAY']}; "
                f"RES={os.environ['EXPYRIMENT_DISPLAY_RESOLUTION']}")

    def beforeEditing(self):
        self.status_text.value = self.get_header_text()

class MainMenuOptionList(npyscreen.MultiLineAction):
    def actionHighlighted(self, act_on_this, key_press):
        selection = act_on_this.split(".")[0] if "." in act_on_this else act_on_this
        
        if "Edit Subject" in act_on_this:
            self.edit_subject()
        elif "Quit" in act_on_this:
            self.parent.parentApp.switchForm(None)
        else:
            self.run_experiment(selection)

    def edit_subject(self):
        # FIX: Manually creating a Popup Form to get input
        current_sub = os.environ['SUBJECT']
        
        # Create a temporary popup window
        F = npyscreen.Popup(name="Edit Configuration")
        # Add a text input widget
        sub_widget = F.add(npyscreen.TitleText, name="Enter SUBJECT id:", value=current_sub)
        # Activate the popup (this blocks until the user presses OK/Enter)
        F.edit()
        
        # Retrieve value after popup closes
        new_sub = sub_widget.value
        
        if new_sub:
            os.environ['SUBJECT'] = new_sub
            #npyscreen.notify_confirm(f"Success! Value updated to {new_sub}", title="Success")
            self.parent.status_text.value = self.parent.get_header_text()
            self.parent.status_text.display()
        else:
            npyscreen.notify_confirm("Change cancelled or empty.", title="Cancelled")
        
        # Force redraw of the main form to update header
        self.parent.display()

    def run_experiment(self, selection_index):
        cmd_suffix = ""
        desc = ""
        
        if selection_index == "2":
            desc = "Calibration"
            cmd_suffix = " --cali 1"
        elif selection_index == "3":
            desc = "Instructions"
            cmd_suffix = " --splash instructions_localizer.csv"
        elif selection_index == "4":
            desc = "Session 1"
            cmd_suffix = " --csv_file session1_localizer_standard.csv"
        elif selection_index == "5":
            desc = "Session 2"
            cmd_suffix = " --csv_file session2_localizer_standard.csv"
        elif selection_index == "6":
            desc = "Session 3"
            cmd_suffix = " --csv_file session3_localizer_standard.csv"
        elif selection_index == "7":
            desc = "Session 4"
            cmd_suffix = " --csv_file session4_localizer_standard.csv"

        if cmd_suffix:
            full_command = CMD_LOCALIZER_BASE + cmd_suffix
            
            npyscreen.blank_terminal()
            #print(f"Running: {desc}")
            #print(full_command)
            
            try:
                subprocess.call(full_command, shell=True)
            except KeyboardInterrupt:
                pass

            # Auto-increment logic
            current_index = self.cursor_line
            if 3 <= current_index < 6:
                self.cursor_line += 1
            elif current_index == 6:
                self.cursor_line += 1
            
            self.parent.display()

if __name__ == "__main__":
    try:
        app = PinelLocalizerApp()
        app.run()
    except KeyboardInterrupt:
        sys.exit(0)
