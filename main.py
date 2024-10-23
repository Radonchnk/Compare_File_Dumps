import os
from customtkinter import *

from gui.dataManager import DataManager
from gui.analyseData import AnalyseData


class App(CTk):
    def __init__(self, *args, **kwargs):
        # Simular structure in other applications
        super().__init__(*args, **kwargs)

        set_appearance_mode("dark")
        set_default_color_theme("green")

        self.title("dont look here")

        # Set size of window
        width = 500
        height = 300

        # Get the screen width and height
        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()

        # Place window in center of screen
        x = (screenWidth - width) // 2
        y = (screenHeight - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

        self.frame = CTkFrame(master=self)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        # Setups main buttons
        self.label = CTkLabel(master=self.frame, text="NFC data manager")
        self.label.grid(row=0, column=0, pady=12, padx=10, columnspan=3)
        self.label.configure(font=("Roboto", 24))

        button1 = CTkButton(master=self.frame, text="Upload .nfc files", command=self.uploadDataMenu,
                            width=200,height=50)
        button1.configure(font=("Roboto", 18))

        button2 = CTkButton(master=self.frame, text="Lettuce begin", width=200, command=self.analyseDataMenu,
                            height=50)
        button2.configure(font=("Roboto", 18))

        # Places buttons
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)

        button1.grid(row=1, column=0, pady=12, padx=(10, 10))
        button2.grid(row=2, column=0, pady=12, padx=(10, 10))

        self.frame.grid_columnconfigure(0, weight=1)

        self.frame.grid_propagate(False)

        # Setup min and max size
        self.minsize(500, 300)
        self.maxsize(800, 500)

        self.data_folder = os.path.join(os.getcwd(), "data")


    def openMainWindow(self):
        # Show the main window
        self.deiconify()

    def uploadDataMenu(self):

        # Hide the main window
        self.withdraw()

        # After PDF conversion and PDF to text conversion start processing
        self.ContinueBook = DataManager(root_instance=self)

    def analyseDataMenu(self):

        # Hide the main window
        self.withdraw()

        # After PDF conversion and PDF to text conversion start processing
        self.ContinueBook = AnalyseData(root_instance=self)


if __name__ == "__main__":
    app = App()
    app.mainloop()
