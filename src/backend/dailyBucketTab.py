import customtkinter
import backendHelperFunctions
import storeBucket
import os
import subprocess

class DailyBucketTab:
    def __init__(self, tab, app):
        self.tab = tab
        self.app = app
        self.createWidgets()
        self.createMainWidgets()
        self.sidebarFrameSwitches = []

    def createSidebarButtons(self, scrollableFrame, folderName):
        dailyBucketFileNames = backendHelperFunctions.getSortedBucketFileNames(folderName)
        
        for i, fileName in enumerate(dailyBucketFileNames):
            button = customtkinter.CTkButton(
                master=scrollableFrame, 
                text=fileName, 
                command=lambda name=fileName: self.openFile(name, folderName)
            )
            button.grid(row=i, column=0, padx=10, pady=(0, 10), sticky="w")
            self.sidebarFrameSwitches.append(button)

    def createWidgets(self):
        self.tab.grid_rowconfigure(5, weight=1)
        self.tab.grid_columnconfigure(0, weight=1)

        self.createRadioFrame(self.tab, ["prod", "stage", "dev"])

        self.dailyEntryDisplay = customtkinter.CTkEntry(self.tab, placeholder_text="Submit daily bucket data", state="disabled", width=300)
        self.dailyEntryDisplay.grid(row=2, column=0, padx=(25, 5), pady=(2, 10), sticky="w")

        self.dailyBucketIDEntry = customtkinter.CTkEntry(self.tab, placeholder_text="Submit daily bucket ID", state="disabled", width=300)
        self.dailyBucketIDEntry.grid(row=4, column=0, padx=(25, 5), pady=(2, 10), sticky="w")

        self.createDailyLabelsAndEntries()

        self.dailyTextbox = customtkinter.CTkTextbox(self.tab, width=250, height=150)
        self.dailyTextbox.configure(state="disabled")
        self.dailyTextbox.grid(row=5, column=0, padx=20, pady=(50, 10), sticky="nsew")

    def createMainWidgets(self):
        self.entryInput = customtkinter.CTkEntry(self.tab, placeholder_text="URL or storeId")
        self.entryInput.grid(row=6, column=0, columnspan=2, padx=(20, 0), pady=(20, 5), sticky="nsew")
        self.entryInput.bind("<KeyRelease>", self.updateEntries)

        self.mainButton = customtkinter.CTkButton(self.tab, text="Submit", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.submit)
        self.mainButton.grid(row=6, column=2, padx=(20, 20), pady=(20, 5), sticky="nsew")

    def createRadioFrame(self, tab, options):
        self.radioFrame = customtkinter.CTkFrame(tab)
        self.radioFrame.grid(row=0, column=0, padx=5, pady=(10, 5), sticky="ew")
        self.radioVarDaily = customtkinter.StringVar(value=options[0])
        for i, text in enumerate(options):
            radio = customtkinter.CTkRadioButton(self.radioFrame, text=text, variable=self.radioVarDaily, value=text, height=20, width=60, radiobutton_width=10, radiobutton_height=10)
            radio.grid(row=0, column=i, padx=2, pady=5, sticky="w")

    def createDailyLabelsAndEntries(self):
        self.tab.grid_rowconfigure(0, weight=0)
        self.tab.grid_rowconfigure(1, weight=0)
        self.tab.grid_rowconfigure(2, weight=0)
        self.tab.grid_rowconfigure(3, weight=0)
        self.tab.grid_rowconfigure(4, weight=0)
        self.tab.grid_rowconfigure(5, weight=1)

        #change names to sth descriptive
        dailyLabel1 = customtkinter.CTkLabel(self.tab, text="1. url:", anchor="w")
        dailyLabel1.grid(row=1, column=0, padx=(25, 5), pady=(20, 2), sticky="w")

        dailyLabel2 = customtkinter.CTkLabel(self.tab, text="2. url with body, create pop to see it...", anchor="w")
        dailyLabel2.grid(row=3, column=0, padx=(25, 5), pady=(10, 2), sticky="w")

    def setDefaultValues(self):
        self.dailyEntryDisplay.configure(state="normal")
        self.dailyEntryDisplay.delete(0, 'end')
        self.dailyEntryDisplay.insert(0, "Default daily bucket value")
        self.dailyEntryDisplay.configure(state="disabled")

        self.dailyBucketIDEntry.configure(state="normal")
        self.dailyBucketIDEntry.delete(0, 'end')
        self.dailyBucketIDEntry.insert(0, "Default converted bucket ID")
        self.dailyBucketIDEntry.configure(state="disabled")

    def updateEntries(self, event=None):
        inputText = self.entryInput.get()
        self.updateEntry(self.dailyEntryDisplay, inputText)
        self.updateEntry(self.dailyBucketIDEntry, backendHelperFunctions.getFilePath(inputText))

        if not inputText:
            self.updateTextboxDaily('', '')

    def updateEntry(self, entry, text):
        entry.configure(state="normal")
        entry.delete(0, 'end')
        entry.insert(0, text)
        entry.configure(state="disabled")

    def updateTextboxDaily(self, message, status):
        self.dailyTextbox.configure(state="normal")
        self.dailyTextbox.delete("1.0", customtkinter.END)

        if status == "success":
            self.dailyTextbox.configure(text_color="green")
        else:
            self.dailyTextbox.configure(text_color="red")

        self.dailyTextbox.insert(customtkinter.END, message)
        self.dailyTextbox.configure(state="disabled")


    def openFile(self, fileName, folder):
        ## add here logic for sending tab info and showing tab info...
        try:
            # Get the directory where the current script (app.py) is located
            script_dir = os.path.dirname(os.path.realpath(__file__))
            
            # Construct the relative file path based on the script's location
            filePath = os.path.join(script_dir, folder, fileName)

            subprocess.Popen(['open', filePath])

            with open(filePath, 'r') as file:
                content = file.read()
                # Display the content in the daily tab's textbox or wherever appropriate
                self.updateTextboxDaily(content, "success")

        except Exception as e:
            print(f"Error handling file {fileName}: {str(e)}")
            self.updateTextboxDaily(f"Error handling file {fileName}", "error")


    def submit(self):
        inputText = self.storeEntryDisplay.get()
        environmentName = self.storeRadioVar.get()
        result = storeBucket.fetchVehicleData(environmentName, inputText)
        self.updateTextboxStore(result['message'], result['status'])

