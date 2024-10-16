import customtkinter
from src.backend.backendHelperFunctions import getSortedBucketFileNames, deleteBucketHistory, createReverseCheckBucketCmd, getFilePath
from src.backend import storeBucket
import os
import subprocess

class StoreBucketTab:
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
        self.tab.grid_rowconfigure(7, weight=1)
        self.tab.grid_columnconfigure(0, weight=1)

        self.storeRadioVar = customtkinter.StringVar(value="prod")
        self.storeRadioVar.trace_add("write", self.onRadioChange)
        self.createStoreRadioFrame(self.tab, self.storeRadioVar, [("Prod", "prod"), ("Stage", "stage"), ("Dev", "dev")])

        self.storeIdPlaceholder = customtkinter.CTkEntry(self.tab, state="disabled", width=300)
        self.storeIdPlaceholder.grid(row=2, column=0, padx=(25, 5), pady=(2, 10), sticky="w")

        self.convertedStoreIdPlaceholder = customtkinter.CTkEntry(self.tab, state="disabled", width=300)
        self.convertedStoreIdPlaceholder.grid(row=4, column=0, padx=(25, 5), pady=(2, 10), sticky="w")

        self.createReverseCheckStoreCmdElements()
        self.createStoreLabels()

        self.storeTextbox = customtkinter.CTkTextbox(self.tab, width=250, height=150)
        self.storeTextbox.configure(state="disabled")
        self.storeTextbox.grid(row=7, column=0, padx=(20,0), pady=(50, 10), sticky="nsew")

    def createReverseCheckStoreCmdElements(self):
        self.reverseCheckFrame = customtkinter.CTkFrame(self.tab)
        self.reverseCheckFrame.grid(row=6, column=0, padx=(25, 5), pady=(2, 10), sticky="w")

        self.reverseCheckFrame.grid_columnconfigure(0, weight=1)
        self.reverseCheckFrame.grid_columnconfigure(1, weight=0)

        self.reverseCheckCmdEntry = customtkinter.CTkEntry(self.reverseCheckFrame, state="disabled", width=600)
        self.reverseCheckCmdEntry.grid(row=0, column=0, sticky="w")

        self.copyButton = customtkinter.CTkButton(self.reverseCheckFrame, text="Copy", command=self.copyReverseCheckCmd, width=50)
        self.copyButton.grid(row=0, column=1, padx=(5, 0), sticky="w")

    def createMainWidgets(self):
        self.entryInput = customtkinter.CTkEntry(self.tab, placeholder_text="storeId")
        self.entryInput.grid(row=8, column=0, columnspan=2, padx=(20, 0), pady=(20, 5), sticky="nsew")
        self.entryInput.bind("<KeyRelease>", self.updateEntries)

        self.mainButton = customtkinter.CTkButton(self.tab, text="Submit", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.submit)
        self.mainButton.grid(row=8, column=2, padx=(20, 20), pady=(20, 5), sticky="nsew")

    def createStoreRadioFrame(self, tab, variable, options):
        self.storeRadioFrame = customtkinter.CTkFrame(tab)
        self.storeRadioFrame.grid(row=0, column=0, padx=5, pady=(10, 5), sticky="ew")
        for i, (text, value) in enumerate(options):
            radio = customtkinter.CTkRadioButton(self.storeRadioFrame, text=text, variable=variable, value=value, height=20, width=60, radiobutton_width=10, radiobutton_height=10)
            radio.grid(row=0, column=i, padx=2, pady=5, sticky="w")

    def createStoreLabels(self):
        self.tab.grid_rowconfigure((0,7), weight=0)
        self.tab.grid_rowconfigure(7, weight=1)

        storeLabel1 = customtkinter.CTkLabel(self.tab, text="1. storeId:", anchor="w")
        storeLabel1.grid(row=1, column=0, padx=(25, 5), pady=(20, 2), sticky="w")

        storeLabel2 = customtkinter.CTkLabel(self.tab, text="2. S3 bucket key (file location)", anchor="w")
        storeLabel2.grid(row=3, column=0, padx=(25, 5), pady=(10, 2), sticky="w")

        reverseCheckCmdLabel = customtkinter.CTkLabel(self.tab, text="Reverse check terminal command", anchor="w")
        reverseCheckCmdLabel.grid(row=5, column=0, padx=(25, 5), pady=(10, 2), sticky="w")

    def copyReverseCheckCmd(self):
        reverseCheckCmd = self.reverseCheckCmdEntry.get()
        self.tab.clipboard_clear()
        self.tab.clipboard_append(reverseCheckCmd)
        self.tab.update()

    def setDefaultstoreBucketEntryValues(self):
        self.storeIdPlaceholder.configure(state="normal")
        self.storeIdPlaceholder.delete(0, "end")
        self.storeIdPlaceholder.insert(0, "Paste the storeId at the bottom input to view")
        self.storeIdPlaceholder.configure(state="readonly")

    def updateEntries(self, event=None):
        inputText = self.entryInput.get().strip()
        self.updateEntry(self.storeIdPlaceholder, inputText)
        self.updateEntry(self.convertedStoreIdPlaceholder, getFilePath(inputText))
        self.updateEntry(self.reverseCheckCmdEntry, createReverseCheckBucketCmd(self.storeRadioVar.get(), self.convertedStoreIdPlaceholder.get(), 'storeBucket'))

        if not inputText:
            self.updateTextboxStore("", "")
            self.updateEntry(self.storeIdPlaceholder, "")
            self.updateEntry(self.convertedStoreIdPlaceholder, "")
            self.updateEntry(self.reverseCheckCmdEntry, "")


    def updateEntry(self, entry, text):
        entry.configure(state="normal")
        entry.delete(0, "end")
        entry.insert(0, text)
        entry.configure(state="readonly")

    def updateTextboxStore(self, message, status):
        self.storeTextbox.configure(state="normal")
        self.storeTextbox.delete("1.0", customtkinter.END)

        if status == "success":
            self.storeTextbox.configure(text_color="green")
        else:
            self.storeTextbox.configure(text_color="red")

        self.storeTextbox.insert(customtkinter.END, message)
        
        # textbox doesnt support readonly type
        # prevents users from typing anything inside the CTkTextbox widget, effectively making it "readonly" from a user interaction perspective.
        self.storeTextbox.bind("<Key>", lambda e: "break")  # Block key presses to prevent typing

        # Allow selecting text and copying using Ctrl+C or Cmd+C
        self.storeTextbox.bind("<Control-c>", lambda e: self.tab.clipboard_append(self.storeTextbox.selection_get()))
        self.storeTextbox.bind("<Command-c>", lambda e: self.tab.clipboard_append(self.storeTextbox.selection_get()))

        self.storeTextbox.configure(state="disabled")


    def openFile(self, fileName, folder):
        try:
            # get the directory where the current script (app.py) is located
            script_dir = os.path.dirname(os.path.realpath(__file__))
            
            filePath = os.path.join(script_dir, folder, fileName)
            filePath = filePath.replace("frontend", "backend") #TODO temp fix due to folder restructuring, improve later

            subprocess.Popen(["open", filePath])

            with open(filePath, "r") as file:
                content = file.read()
                self.updateExistingVehicleEntries(fileName.split("_")[0], content, "success")


        except Exception as e:
            print(f"Error handling file {fileName}: {str(e)}")
            self.updateTextboxStore(f"Error handling file {fileName}", "error")

    # update vehice entries based on opened file
    def updateExistingVehicleEntries(self, fileName, content, status):
        self.updateTextboxStore(content, status)
        self.updateEntry(self.storeIdPlaceholder, fileName)
        self.updateEntry(self.convertedStoreIdPlaceholder, getFilePath(fileName))

    def onRadioChange(self, *args):
        self.updateEntry(self.reverseCheckCmdEntry, createReverseCheckBucketCmd(self.storeRadioVar.get(), self.convertedStoreIdPlaceholder.get(), 'storeBucket'))


    def deleteStoreBucketHistory(self, folderName, scrollableFrame):
        result = deleteBucketHistory(self, folderName)
        self.updateTextboxStore(result["message"], result["status"])

        if (result["status"] == "success"):
            self.createSidebarButtons(scrollableFrame, folderName)

    def submit(self):
        storeId = self.storeIdPlaceholder.get().strip()
        environmentName = self.storeRadioVar.get()
        result = storeBucket.fetchVehicleData(environmentName, storeId)
        self.updateTextboxStore(result["message"], result["status"])
