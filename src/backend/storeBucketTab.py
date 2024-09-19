import customtkinter
import backendHelperFunctions
import storeBucket
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
        self.tab.grid_rowconfigure(7, weight=1)
        self.tab.grid_columnconfigure(0, weight=1)

        self.storeRadioVar = customtkinter.StringVar(value="prod")
        self.createStoreRadioFrame(self.tab, self.storeRadioVar, [("Prod", "prod"), ("Stage", "stage"), ("Dev", "dev")])

        self.storeIdPlaceholder = customtkinter.CTkEntry(self.tab, placeholder_text="Submit storeId to view", state="disabled", width=300)
        self.storeIdPlaceholder.grid(row=2, column=0, padx=(25, 5), pady=(2, 10), sticky="w")

        self.convertedStoreIdPlaceholder = customtkinter.CTkEntry(self.tab, placeholder_text="Submit storeId to view", state="disabled", width=300)
        self.convertedStoreIdPlaceholder.grid(row=4, column=0, padx=(25, 5), pady=(2, 10), sticky="w")

        self.reverseCheckCmdEntry = customtkinter.CTkEntry(self.tab, placeholder_text="Reverse check command", state="disabled", width=600)
        self.reverseCheckCmdEntry.grid(row=6, column=0, padx=(25, 5), pady=(2, 10), sticky="w")

        self.createStoreLabelsAndEntries()

        self.storeTextbox = customtkinter.CTkTextbox(self.tab, width=250, height=150)
        self.storeTextbox.configure(state="disabled")
        self.storeTextbox.grid(row=7, column=0, padx=20, pady=(50, 10), sticky="nsew")

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

    def createStoreLabelsAndEntries(self):
        self.tab.grid_rowconfigure((0,7), weight=0)
        self.tab.grid_rowconfigure(7, weight=1)


        storeLabel1 = customtkinter.CTkLabel(self.tab, text="1. storeId:", anchor="w")
        storeLabel1.grid(row=1, column=0, padx=(25, 5), pady=(20, 2), sticky="w")

        storeLabel2 = customtkinter.CTkLabel(self.tab, text="2. S3 bucket key (file location)", anchor="w")
        storeLabel2.grid(row=3, column=0, padx=(25, 5), pady=(10, 2), sticky="w")

        reverseCheckCmdLabel = customtkinter.CTkLabel(self.tab, text="ADDITIONAL: reverse check terminal command", anchor="w")
        reverseCheckCmdLabel.grid(row=5, column=0, padx=(25, 5), pady=(10, 2), sticky="w")

    def updateEntries(self, event=None):
        inputText = self.entryInput.get()
        self.updateEntry(self.storeIdPlaceholder, inputText)
        self.updateEntry(self.convertedStoreIdPlaceholder, backendHelperFunctions.getFilePath(inputText))
        self.updateEntry(self.reverseCheckCmdEntry, backendHelperFunctions.createReverseCheckStoreCmd(self.storeRadioVar.get(), self.convertedStoreIdPlaceholder.get()))

        if not inputText:
            self.updateTextboxStore('', '')

    def updateEntry(self, entry, text):
        entry.configure(state="normal")
        entry.delete(0, 'end')
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
        self.storeTextbox.configure(state="readonly")


    def openFile(self, fileName, folder):
        try:
            # get the directory where the current script (app.py) is located
            script_dir = os.path.dirname(os.path.realpath(__file__))
            
            filePath = os.path.join(script_dir, folder, fileName)

            subprocess.Popen(['open', filePath])

            with open(filePath, 'r') as file:
                content = file.read()
                self.updateExistingVehicleEntries(fileName.split("_")[0], content, "success")


        except Exception as e:
            print(f"Error handling file {fileName}: {str(e)}")
            self.updateTextboxStore(f"Error handling file {fileName}", "error")

    # update vehice entries based on opened file
    def updateExistingVehicleEntries(self, fileName, content, status):
        self.updateTextboxStore(content, status)
        self.updateEntry(self.storeIdPlaceholder, fileName)
        self.updateEntry(self.convertedStoreIdPlaceholder, backendHelperFunctions.getFilePath(fileName))


    def deleteStoreBucketHistory(self, folderName, scrollableFrame):
        result = backendHelperFunctions.deleteBucketHistory(self, folderName)
        self.updateTextboxStore(result['message'], result['status'])

        if (result["status"] == "success"):
            self.createSidebarButtons(scrollableFrame, folderName)

    def submit(self):
        storeId = self.storeIdPlaceholder.get()
        environmentName = self.storeRadioVar.get()
        result = storeBucket.fetchVehicleData(environmentName, storeId)
        self.updateTextboxStore(result['message'], result['status'])
