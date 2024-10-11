import customtkinter
from src.backend.backendHelperFunctions import getSortedBucketFileNames, deleteBucketHistory, generateDailyBucketParams, createReverseCheckBucketCmd
from src.backend import dailyBucket
import os
import subprocess
import datetime

class DailyBucketTab:
    def __init__(self, tab, app):
        self.tab = tab
        self.app = app
        self.createWidgets()
        self.createMainWidgets()
        self.sidebarFrameSwitches = []

    def createSidebarButtons(self, scrollableFrame, folderName):
        dailyBucketFileNames = getSortedBucketFileNames(folderName)
        
        for i, fileName in enumerate(dailyBucketFileNames):
            button = customtkinter.CTkButton(
                master=scrollableFrame, 
                text=fileName, 
                command=lambda name=fileName: self.openFile(name, folderName)
            )
            button.grid(row=i, column=0, padx=10, pady=(0, 10), sticky="w")
            self.sidebarFrameSwitches.append(button)

    def createWidgets(self):
        self.tab.grid_rowconfigure(11, weight=1)
        self.tab.grid_columnconfigure((0,1), weight=1)

        self.dailyRadioVar = customtkinter.StringVar(value="prod")
        self.dailyRadioVar.trace_add("write", self.onRadioChange)
        self.createDailyRadioFrame(self.tab, self.dailyRadioVar, [("Prod", "prod"), ("Stage", "stage"), ("Dev", "dev")])

        self.dailyEntryDisplay = customtkinter.CTkEntry(self.tab, state="disabled", width=400)
        self.dailyEntryDisplay.grid(row=2, column=0, padx=(25, 5), pady=(2, 10), sticky="w")

        self.dailyUrlWithBodyAndButtonFrame = customtkinter.CTkFrame(self.tab)
        self.dailyUrlWithBodyAndButtonFrame.grid(row=4, column=0, padx=(25, 5), pady=(2, 10), sticky="w")

        self.dailyUrlWithBody = customtkinter.CTkEntry(self.dailyUrlWithBodyAndButtonFrame, state="disabled", width=400)
        self.dailyUrlWithBody.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="w")

        self.dailyBucketPopupButton = customtkinter.CTkButton(self.dailyUrlWithBodyAndButtonFrame, text="Show all", command=self.showDailyBucketPopup, width=50)
        self.dailyBucketPopupButton.grid(row=0, column=1, padx=(5 ,0), pady=(0, 0), sticky="w")

        self.hashedUrlAndBodyEntry = customtkinter.CTkEntry(self.tab, state="disabled", width=400)
        self.hashedUrlAndBodyEntry.grid(row=6, column=0, padx=(25, 5), pady=(2, 10), sticky="w")

        self.dateAndHashedUrlEntry = customtkinter.CTkEntry(self.tab, state="disabled", width=400)
        self.dateAndHashedUrlEntry.grid(row=8, column=0, padx=(25, 5), pady=(2, 10), sticky="w")

        self.createReverseCheckCmdElements()
        self.createDailyBucketLabels()

        self.dailyTextbox = customtkinter.CTkTextbox(self.tab, width=700, height=150)
        self.dailyTextbox.configure(state="disabled")
        self.dailyTextbox.grid(row=11, column=0, padx=(20,5), pady=(50, 10), sticky="nsew")

    def createReverseCheckCmdElements(self):
        self.reverseDailyCheckFrame = customtkinter.CTkFrame(self.tab)
        self.reverseDailyCheckFrame.grid(row=10, column=0, padx=(25, 5), pady=(2, 10), sticky="w")

        self.reverseDailyCheckFrame.grid_columnconfigure(0, weight=1)
        self.reverseDailyCheckFrame.grid_columnconfigure(1, weight=0)

        self.reverseDailyCheckCmdEntry = customtkinter.CTkEntry(self.reverseDailyCheckFrame, state="disabled", width=700)
        self.reverseDailyCheckCmdEntry.grid(row=0, column=0, sticky="w")

        self.copyDailyReverseCheckButton = customtkinter.CTkButton(self.reverseDailyCheckFrame, text="Copy", command=self.copyReverseCheckCmd, width=50)
        self.copyDailyReverseCheckButton.grid(row=0, column=1, padx=(5, 0), sticky="w")

    def createMainWidgets(self):
        self.tab.grid_columnconfigure(0, weight=2)
        self.tab.grid_columnconfigure(1, weight=1, minsize=110)  # date column with a minimum width
        self.tab.grid_columnconfigure(2, weight=0)

        self.entryInput = customtkinter.CTkEntry(self.tab, placeholder_text="{url}_{body}", width=700)
        self.entryInput.grid(row=12, column=0, padx=(20, 5), pady=(20, 5), sticky="w")
        self.entryInput.bind("<KeyRelease>", self.updateEntries)

        self.dateInput = customtkinter.CTkEntry(self.tab, placeholder_text="YYYYMMDD", width=150)
        self.dateInput.grid(row=12, column=1, padx=(5, 10), pady=(20, 5), sticky="ew")
        self.dateInput.insert(0, self.getCurrentDate())
        self.dateInput.bind("<KeyRelease>", self.updateEntries)

        self.mainButton = customtkinter.CTkButton(self.tab, text="Submit", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.submit)
        self.mainButton.grid(row=12, column=2, padx=(20, 20), pady=(20, 5), sticky="nsew")

    def createDailyRadioFrame(self, tab, variable, options):
        self.dailyRadioFrame = customtkinter.CTkFrame(tab)
        self.dailyRadioFrame.grid(row=0, column=0, padx=5, pady=(10, 5), sticky="ew")
        for i, (text, value) in enumerate(options):
            radio = customtkinter.CTkRadioButton(self.dailyRadioFrame, text=text, variable=variable, value=value, height=20, width=60, radiobutton_width=10, radiobutton_height=10)
            radio.grid(row=0, column=i, padx=2, pady=5, sticky="w")

    def createDailyBucketLabels(self):
        self.tab.grid_rowconfigure((0,10), weight=0)
        self.tab.grid_rowconfigure(11, weight=1)

        dailyEntryDisplay = customtkinter.CTkLabel(self.tab, text="1. url", anchor="w")
        dailyEntryDisplay.grid(row=1, column=0, padx=(25, 5), pady=(20, 2), sticky="w")

        dailyUrlWithBody = customtkinter.CTkLabel(self.tab, text="2. url with body", anchor="w")
        dailyUrlWithBody.grid(row=3, column=0, padx=(25, 5), pady=(10, 2), sticky="w")

        hashedUrlAndBodyEntry = customtkinter.CTkLabel(self.tab, text="3. hashed url and body", anchor="w")
        hashedUrlAndBodyEntry.grid(row=5, column=0, padx=(25, 5), pady=(10, 2), sticky="w")

        dateAndHashedUrlEntry = customtkinter.CTkLabel(self.tab, text="4. date and hashed url with body", anchor="w")
        dateAndHashedUrlEntry.grid(row=7, column=0, padx=(25, 5), pady=(10, 2), sticky="w")

        reverseDailyCheckCmdEntry = customtkinter.CTkLabel(self.tab, text="Reverse check terminal command", anchor="w")
        reverseDailyCheckCmdEntry.grid(row=9, column=0, padx=(25, 5), pady=(10, 2), sticky="w")

    def setDefaulDailyBucketEntryValues(self):
        self.dailyEntryDisplay.configure(state="normal")
        self.dailyEntryDisplay.delete(0, "end")
        self.dailyEntryDisplay.insert(0, "Paste the url at the bottom input to view")
        self.dailyEntryDisplay.configure(state="readonly")

    def copyReverseCheckCmd(self):
        reverseCheckCmd = self.reverseDailyCheckCmdEntry.get()
        self.tab.clipboard_clear()
        self.tab.clipboard_append(reverseCheckCmd)
        self.tab.update()

    def onRadioChange(self, *args):
        self.updateEntry(self.reverseDailyCheckCmdEntry, createReverseCheckBucketCmd(self.dailyRadioVar.get(), self.dateAndHashedUrlEntry.get(), 'dailyBucket'))

    def updateEntries(self, event=None):
        urlWithBody = self.entryInput.get().strip()
        url, vehicleUrlBody = (urlWithBody.rsplit("_", 1) if "_" in urlWithBody else (urlWithBody, "undefined")) #TODO this is bad practice, improve
        dateInput = self.dateInput.get()
        self.updateEntry(self.dailyEntryDisplay, url)

        vehicleUrlWithBody = f"{url}_{vehicleUrlBody}" #ovo staviti u backend funkciju zbog logike s undefiend?
    
        self.updateEntry(self.dailyUrlWithBody, vehicleUrlWithBody)
    
        dailyBucketParams = generateDailyBucketParams(url, vehicleUrlBody, dateInput)
        self.updateEntry(self.hashedUrlAndBodyEntry, dailyBucketParams["vehicleUrlHashed"])
        self.updateEntry(self.dateAndHashedUrlEntry, dailyBucketParams["dailyBucketKeyPrefix"])

        self.updateEntry(self.reverseDailyCheckCmdEntry, createReverseCheckBucketCmd(self.dailyRadioVar.get(), self.dateAndHashedUrlEntry.get(), 'dailyBucket'))
       
        if not urlWithBody:
            self.updateTextboxDaily("", "")
            self.updateEntry(self.dailyUrlWithBody, "")
            self.updateEntry(self.hashedUrlAndBodyEntry, "")
            self.updateEntry(self.dateAndHashedUrlEntry, "")
            self.updateEntry(self.reverseDailyCheckCmdEntry, "")

    def updateEntry(self, entry, text):
        entry.configure(state="normal")
        entry.delete(0, "end")
        entry.insert(0, text)
        entry.configure(state="readonly")

    def updateTextboxDaily(self, message, status):
        self.dailyTextbox.configure(state="normal")
        self.dailyTextbox.delete("1.0", customtkinter.END)

        if status == "success":
            self.dailyTextbox.configure(text_color="green")
        else:
            self.dailyTextbox.configure(text_color="red")

        self.dailyTextbox.insert(customtkinter.END, message)

        # textbox doesnt support readonly type
        # prevents users from typing anything inside the CTkTextbox widget, effectively making it "readonly" from a user interaction perspective.
        self.dailyTextbox.bind("<Key>", lambda e: "break")  # Block key presses to prevent typing

        # Allow selecting text and copying using Ctrl+C or Cmd+C
        self.dailyTextbox.bind("<Control-c>", lambda e: self.tab.clipboard_append(self.dailyTextbox.selection_get()))
        self.dailyTextbox.bind("<Command-c>", lambda e: self.tab.clipboard_append(self.dailyTextbox.selection_get()))

        self.dailyTextbox.configure(state="disabled")


    def openFile(self, fileName, folder):
        try:
            # get the directory where the current script (app.py) is located
            script_dir = os.path.dirname(os.path.realpath(__file__))
            
            # construct the relative file path based on the script"s location
            filePath = os.path.join(script_dir, folder, fileName)
            filePath = filePath.replace("frontend", "backend") #TODO temp fix due to folder restructuring, improve later

            subprocess.Popen(["open", filePath])

            with open(filePath, "r") as file:
                content = file.read()
                # display the content in the daily tab"s textbox
                self.updateTextboxDaily(content, "success")

        except Exception as e:
            print(f"Error handling file {fileName}: {str(e)}")
            self.updateTextboxDaily(f"Error handling file {fileName}", "error")


    def showDailyBucketPopup(self):
        dailyBucketEntryText = self.dailyUrlWithBody.get()
        popup = customtkinter.CTkToplevel(self.tab)
        popup.geometry("400x200")
        popup.title("URL with Body")

        message_label = customtkinter.CTkLabel(popup, text=dailyBucketEntryText, wraplength=350)
        message_label.pack(padx=20, pady=20)

    def deleteDailyBucketHistory(self, folderName, scrollableFrame):
        result = deleteBucketHistory(self, folderName)
        self.updateTextboxDaily(result["message"], result["status"])

        if (result["status"] == "success"):
            self.createSidebarButtons(scrollableFrame, folderName)

    # Returns today's date in "YYYYMMDD" format
    def getCurrentDate(self):
        return datetime.datetime.now().strftime("%Y%m%d")

    def submit(self):
        urlWithBody = self.entryInput.get().strip()
        url, vehicleUrlBody = (urlWithBody.rsplit("_", 1) if "_" in urlWithBody else (urlWithBody, None))
        environmentName = self.dailyRadioVar.get()
        date = self.dateInput.get()
    
        result = dailyBucket.fetchVehicleRawResponse(environmentName, date, url, vehicleUrlBody) #TODO test what happens if no date is entered, possibly create restriction
        self.updateTextboxDaily(result["message"], result["status"])

