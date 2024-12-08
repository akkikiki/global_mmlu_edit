import tkinter as tk
from tkinter import filedialog, simpledialog
import json

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("JSONL Editor")
        self.data1 = []
        self.data2 = []
        self.current_index = 0
        self.edited_data1 = []
        self.edited_data2 = []

        self.file_frame = tk.Frame(self)
        self.file_frame.pack(pady=10)

        self.open_button1 = tk.Button(self.file_frame, text="Open File 1", command=self.open_file1)
        self.open_button1.pack(side=tk.LEFT, padx=5)

        self.open_button2 = tk.Button(self.file_frame, text="Open File 2", command=self.open_file2)
        self.open_button2.pack(side=tk.LEFT, padx=5)

        self.data_frame = tk.Frame(self)
        self.data_frame.pack(pady=10)

        self.label1 = tk.Label(self.data_frame, text="Data 1:")
        self.label1.pack()

        self.text1 = tk.Text(self.data_frame, height=10, width=50)
        self.text1.pack(pady=5)

        self.label2 = tk.Label(self.data_frame, text="Data 2:")
        self.label2.pack()

        self.text2 = tk.Text(self.data_frame, height=10, width=50)
        self.text2.pack(pady=5)

        self.control_frame = tk.Frame(self)
        self.control_frame.pack(pady=10)

        self.prev_button = tk.Button(self.control_frame, text="Previous", command=self.show_prev)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(self.control_frame, text="Next", command=self.show_next)
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.jump_button = tk.Button(self.control_frame, text="Jump to Index", command=self.jump_to_index)
        self.jump_button.pack(side=tk.LEFT, padx=5)

        self.index_label = tk.Label(self.control_frame, text=f"Current Index: {self.current_index}")
        self.index_label.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(self.control_frame, text="Save", command=self.save_data)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.export_button = tk.Button(self.control_frame, text="Export", command=self.export_data)
        self.export_button.pack(side=tk.LEFT, padx=5)

        self.exit_button = tk.Button(self.control_frame, text="Exit", command=self.quit)
        self.exit_button.pack(side=tk.LEFT, padx=5)

    def update_index_label(self):
        self.index_label.config(text=f"Current Index: {self.current_index}")

    def open_file1(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                self.data1 = [json.loads(line) for line in f]
            for data1 in self.data1:
                if "is_edited" in self.data1 and not self.data1["is_edited"]:
                    data1["is_edited"] = False
            self.edited_data1 = self.data1.copy()
            self.show_data()

    def open_file2(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                self.data2 = [json.loads(line) for line in f]
            for data2 in self.data2:
                if "is_edited" in self.data2 and not self.data2["is_edited"]:
                    data2["is_edited"] = False
            self.edited_data2 = self.data2.copy()
            self.show_data()

    def show_data(self):
        if self.data1 and self.data2:
            data1 = json.dumps(self.edited_data1[self.current_index], ensure_ascii=False, indent=2)
            data2 = json.dumps(self.edited_data2[self.current_index], ensure_ascii=False, indent=2)
            self.text1.delete("1.0", tk.END)
            self.text1.insert(tk.END, data1)
            self.text2.delete("1.0", tk.END)
            self.text2.insert(tk.END, data2)

    def show_prev(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_data()
            self.update_index_label()
    
    def show_next(self):
        if self.current_index < min(len(self.data1), len(self.data2)) - 1:
            self.current_index += 1
            self.show_data()
            self.update_index_label()

    def jump_to_index(self):
        index_str = simpledialog.askstring("Jump to Index", "Enter the index number")
        if index_str:
            try:
                index = int(index_str)
                if 0 <= index < min(len(self.data1), len(self.data2)):
                    self.current_index = index
                    self.show_data()
                    self.update_index_label()
                else:
                    tk.messagebox.showerror("Error", "Invalid index number")
            except ValueError:
                tk.messagebox.showerror("Error", "Invalid input")

    def save_data(self):
        data1_str = self.text1.get("1.0", tk.END).strip()
        try:
            self.edited_data1[self.current_index] = json.loads(data1_str)
            self.edited_data1[self.current_index]["is_edited"] = True
        except json.JSONDecodeError:
            tk.messagebox.showerror("Error", "Invalid JSON data")
            return
        tk.messagebox.showinfo("Data Saved", "The current edited data has been saved.")

    def export_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".jsonl")
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                for data1 in self.edited_data1:
                    f.write(json.dumps(data1, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    app = App()
    app.mainloop()
