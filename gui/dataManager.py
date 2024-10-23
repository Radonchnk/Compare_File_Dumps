from customtkinter import *

class DataManager(CTk):
    def __init__(self, root_instance, *args, **kwargs):
        # Simular structure in other applications
        super().__init__(*args, **kwargs)

        self.root_instance = root_instance

        set_appearance_mode("dark")
        set_default_color_theme("green")

        self.title("Continue book")

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

        # Bind close button to goBack function
        self.protocol("WM_DELETE_WINDOW", self.goBackEvent)

        # Setups main buttons

        # Places buttons
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)

        self.frame.grid_columnconfigure(0, weight=1)

        self.frame.grid_propagate(False)

        # Setup min and max size
        self.minsize(500, 300)
        self.maxsize(800, 500)

        # Default data folder
        if not os.path.exists(self.root_instance.data_folder):
            os.makedirs(self.root_instance.data_folder)
        self.renderMenu()

    def goBackEvent(self):
        # Call the method in the root instance to show the main window
        self.root_instance.openMainWindow()

        # Close the window
        self.destroy()

    def renderMenu(self):
        # Button to select data folder
        self.folder_button = CTkButton(self.frame, text="Select Data Folder", command=self.selectDataFolder)
        self.folder_button.grid(row=1, column=0, pady=10, padx=10)

        # Label to display selected folder
        self.folder_label = CTkLabel(self.frame, text=f"Current Data Folder: {self.root_instance.data_folder}", wraplength=400)
        self.folder_label.grid(row=2, column=0, pady=10, padx=10)

    def selectDataFolder(self):
        # Open a folder selection dialog
        selected_folder = filedialog.askdirectory(initialdir=os.getcwd(), title="Select Data Folder")

        # If a folder is selected, update the data folder
        if selected_folder:
            self.root_instance.data_folder = selected_folder

        # Update the label with the new folder
        self.folder_label.configure(text=f"Current Data Folder: {self.root_instance.data_folder}")