import os
import tkinter as tk  # Use the Tkinter library for the Text widget
import customtkinter as ctk

class FileLabel(ctk.CTkFrame):  # Inherit from CTkFrame instead of CTk
    def __init__(self, master=None, root_data=None, label1_text="Label 1", label2_text="Label 2", file_path=None, textbox_height=800, textbox_width=300):
        super().__init__(master)

        self.root_data = root_data
        self.file_path = file_path

        # Create Checkbox
        self.checkbox_var = ctk.BooleanVar()
        self.checkbox = ctk.CTkCheckBox(self, text=label1_text, variable=self.checkbox_var, command=self.toggle_textbox)
        self.checkbox.grid(row=0, column=0, sticky="ew", padx=10)

        # Create Label 2
        self.label2 = ctk.CTkLabel(self, text=label2_text)
        self.label2.grid(row=1, column=0, sticky="ew", padx=10)

        # Center align labels
        self.checkbox.grid_configure(pady=10)
        self.label2.grid_configure(pady=10)

        # Create scrollable textbox frame
        self.textbox_frame = ctk.CTkFrame(self)
        self.textbox_frame.grid(row=2, column=0, pady=10, sticky="nsew")

        # Scrollable area for the Text widget
        self.text_scrollbar = tk.Scrollbar(self.textbox_frame)
        self.text_scrollbar.pack(side="right", fill="y")

        # Set up the size of the textbox with configurable height and width
        self.scrollable_textbox = tk.Text(self.textbox_frame, height=textbox_height, width=textbox_width, wrap="word", yscrollcommand=self.text_scrollbar.set)
        self.scrollable_textbox.pack(fill="both", expand=True)
        self.text_scrollbar.config(command=self.scrollable_textbox.yview)

        if file_path:
            if os.path.exists(file_path):
                self.load_file_content(file_path)

        # Initially hide the textbox frame
        self.textbox_frame.grid_remove()  # Hide the textbox frame

        # Make sure the layout expands properly
        self.grid_columnconfigure(0, weight=1)

    def toggle_textbox(self):
        """Show/hide the scrollable textbox based on checkbox status."""
        if self.checkbox_var.get():
            self.textbox_frame.grid()  # Show the textbox frame
            self.root_data.opened_files.append([self.file_path, self])
            self.root_data.highlight_differences()
        else:
            self.textbox_frame.grid_remove()  # Hide the textbox frame
            # Iterate over opened_files to find the one containing self.file_path
            for item in self.root_data.opened_files:
                if item[0] == self.file_path:
                    self.root_data.opened_files.remove(item)
                    break  # Stop after removing the first match

            self.root_data.highlight_differences()

    def load_file_content(self, file_path):
        """Load file content into the scrollable textbox."""
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                self.scrollable_textbox.insert("1.0", content)  # Insert content at the start
        except Exception as e:
            self.scrollable_textbox.insert("1.0", f"Error loading file: {e}")

    def highlight_text(self, line, start_char, end_char, color="yellow"):
        """
        Highlight a specific range of text in the textbox with a specified color.

        :param line: The line number (1-based)
        :param start_char: The starting character index (0-based)
        :param end_char: The ending character index (0-based)
        :param color: The color for highlighting
        """
        tag_name = f"highlight_{line}_{start_char}_{end_char}"
        self.scrollable_textbox.tag_configure(tag_name, background=color)

        # Create the range to highlight using text widget's indices (line.start, line.end)
        start_index = f"{line}.{start_char}"
        end_index = f"{line}.{end_char}"

        self.scrollable_textbox.tag_add(tag_name, start_index, end_index)#

    def highlight_text_bunch(self, data):
        for line, start_char, end_char, color in data:
            self.highlight_text(line=line, start_char=start_char, end_char=end_char, color=color)


# Test code to create the widget
if __name__ == "__main__":
    root = ctk.CTk()

    # Create a scrollable frame
    scrollable_frame = ctk.CTkScrollableFrame(root)
    scrollable_frame.pack(fill="both", expand=True)

    # Create and add FileLabel to the scrollable frame
    for i in range(2):
        # Customize textbox size: height 10 lines, width 40 characters
        file_label = FileLabel(scrollable_frame, label1_text=f"File {i + 1}", label2_text="Test Folder", textbox_height=10, textbox_width=40)
        file_label.grid(row=i, column=0, sticky="nsew", padx=10, pady=10)  # Use sticky="nsew" to make it expand

        # Insert example text into the scrollable textbox
        file_label.scrollable_textbox.insert("1.0", f"This is line 1 of file {i + 1}.\nThis is line 2 of file {i + 1}.\nThis is line 3 of file {i + 1}.\n""1.0", f"This is line 1 of file {i + 1}.\nThis is line 2 of file {i + 1}.\nThis is line 3 of file {i + 1}.\n""1.0", f"This is line 1 of file {i + 1}.\nThis is line 2 of file {i + 1}.\nThis is line 3 of file {i + 1}.\n""1.0", f"This is line 1 of file {i + 1}.\nThis is line 2 of file {i + 1}.\nThis is line 3 of file {i + 1}.\n""1.0", f"This is line 1 of file {i + 1}.\nThis is line 2 of file {i + 1}.\nThis is line 3 of file {i + 1}.\n""1.0", f"This is line 1 of file {i + 1}.\nThis is line 2 of file {i + 1}.\nThis is line 3 of file {i + 1}.\n""1.0", f"This is line 1 of file {i + 1}.\nThis is line 2 of file {i + 1}.\nThis is line 3 of file {i + 1}.\n""1.0", f"This is line 1 of file {i + 1}.\nThis is line 2 of file {i + 1}.\nThis is line 3 of file {i + 1}.\n""1.0", f"This is line 1 of file {i + 1}.\nThis is line 2 of file {i + 1}.\nThis is line 3 of file {i + 1}.\n""1.0", f"This is line 1 of file {i + 1}.\nThis is line 2 of file {i + 1}.\nThis is line 3 of file {i + 1}.\n")

        # Highlight specific characters in line 1 and line 2 with different colors
        file_label.highlight_text(line=1, start_char=8, end_char=13, color="yellow")  # Highlight "line 1"
        file_label.highlight_text(line=2, start_char=8, end_char=13, color="cyan")    # Highlight "line 2"
        file_label.highlight_text(line=3, start_char=8, end_char=13, color="green")   # Highlight "line 3"

    # Ensure that the columns expand in the scrollable frame
    scrollable_frame.grid_columnconfigure(0, weight=1)

    root.geometry("600x400")
    root.mainloop()
