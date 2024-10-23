import os
from customtkinter import *
from gui.FileLable import FileLabel
import itertools


class AnalyseData(CTk):
    def __init__(self, root_instance, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.root_instance = root_instance
        self.opened_files = []

        set_appearance_mode("dark")
        set_default_color_theme("green")

        self.title("madness")

        # Get the screen width and height dynamically
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Set the window size to the full screen but not in fullscreen mode
        self.geometry(f"{screen_width}x{screen_height}")

        # Bind close button to goBack function
        self.protocol("WM_DELETE_WINDOW", self.goBackEvent)

        # Create main frame to hold everything
        self.frame = CTkFrame(master=self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Make the main frame take the entire screen space
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure([0, 1, 2, 3], weight=1)

        # Default data folder
        if not os.path.exists(self.root_instance.data_folder):
            os.makedirs(self.root_instance.data_folder)

        # Call the renderMenu function to populate the UI
        self.renderMenu()

    def renderMenu(self):
        scrollable_frames = [None] * 4
        data_folder = self.root_instance.data_folder

        # Gather data
        data = [(root, dirs, files) for root, dirs, files in os.walk(data_folder)]

        # Flatten the data into a list of (root, file) pairs, where each file is represented by its folder and name
        flat_files = []
        for root, dirs, files in data:
            for file in files:
                file_path = os.path.join(root, file)
                flat_files.append((root, file))

        # Split flat_files into 4 roughly equal parts
        def split_into_chunks(lst, n):
            avg = len(lst) / float(n)
            out = []
            last = 0.0
            while last < len(lst):
                out.append(lst[int(last):int(last + avg)])
                last += avg
            return out

        # Split the files into 4 chunks
        split_files = split_into_chunks(flat_files, 4)

        # Create 4 scrollable frames and populate each with its chunk of files
        for index, files_per_column in enumerate(split_files):
            # Create a scrollable frame for the FileLabels
            scrollable_frames[index] = CTkScrollableFrame(self.frame)
            scrollable_frames[index].grid(row=0, column=index, sticky="nsew")

            # Recursively walk through the split files for this column
            row = 0
            for root, file in files_per_column:
                label2_text = os.path.basename(root)  # The folder name
                file_path = os.path.join(root, file)
                label1_text = file  # The file name

                # Create and add the FileLabel widget to the scrollable frame
                file_label = FileLabel(
                    scrollable_frames[index],  # Pass the scrollable frame as the parent
                    root_data=self,
                    label1_text=label1_text,
                    label2_text=label2_text,
                    file_path=file_path,
                    #textbox_width=self.winfo_screenwidth() // 4 - 50,  # Adjust textbox width for each column
                    textbox_height = 100,
                    textbox_width = 53
                )
                file_label.grid(row=row, column=0, sticky="nsew", padx=1, pady=1)
                row += 1

    def split_array_in_four(self, arr):
        # Calculate the length of each chunk
        n = len(arr)
        chunk_size = n // 4
        remainder = n % 4

        # Create four sub-arrays
        sub_arrays = []
        start = 0

        for i in range(4):
            # Calculate the end of the current chunk
            end = start + chunk_size + (1 if remainder > 0 else 0)
            sub_arrays.append(arr[start:end])
            start = end
            remainder -= 1  # Decrease remainder to evenly distribute extra elements

        return sub_arrays

    def highlight_differences(self):
        changes = []

        # Read the content of each file into a dictionary
        file_contents = {}

        for file, label in self.opened_files:
            try:
                with open(file, 'r') as f:
                    file_contents[file] = f.readlines()  # Store lines in a list
            except Exception as e:
                print(f"Error reading file {file}: {e}")
                return  # Exit if any file can't be read

        # Find the maximum number of lines across all files
        max_lines = max(len(lines) for lines in file_contents.values())
        difference_count = {}  # To count differences for each bit position

        # Compare each line across files
        for line_num in range(max_lines):
            reference_file = self.opened_files[0][0]  # Get the first file for reference
            reference_line = file_contents[reference_file][line_num].strip() if line_num < len(
                file_contents[reference_file]) else ""

            # Compare with each subsequent file
            for file, label in self.opened_files[1:]:
                current_line = file_contents[file][line_num].strip() if line_num < len(file_contents[file]) else ""
                max_length = max(len(reference_line), len(current_line))

                for i in range(max_length):
                    ref_char = reference_line[i] if i < len(reference_line) else ""
                    curr_char = current_line[i] if i < len(current_line) else ""

                    if ref_char != curr_char:  # If characters differ
                        # Increment the count for this position
                        if i not in difference_count:
                            difference_count[i] = 0
                        difference_count[i] += 1

                        # Add to changes array with correct indices
                        start_char = i
                        end_char = i + 1  # Highlighting the single character
                        changes.append(
                            (line_num + 1, start_char, end_char, file))  # Append file for later color calculation

        # Calculate colors based on difference counts and highlight the differences
        for line, start_char, end_char, file in changes:
            # Get the count of differences for this position
            count = difference_count.get(start_char, 0)

            # Determine color intensity
            if count > 0:
                # Calculate color based on the count
                intensity = min(count * 25, 255)  # Cap the intensity at 255
                # Calculate the RGB values
                red = min(255, 255)  # Always 255 for red
                green = max(0, 255 - intensity)  # Decrease green as the count increases

                color = f'#{red:02x}{green:02x}00'  # Construct the hex color string
            else:
                color = "red"  # Default color for no differences

            # Highlight in the respective textbox
            for f, lbl in self.opened_files:
                if f == file:
                    lbl.highlight_text(line, start_char, end_char, color)  # Highlight in the respective textbox

        print("Differences highlighted:", changes)

    def goBackEvent(self):
        # Call the method in the root instance to show the main window
        self.root_instance.openMainWindow()

        # Close the window
        self.destroy()
