#!/usr/bin/env python3
"""
GUI Launcher for Theater Auftakt Audio Processing Scripts
A simple graphical interface for non-technical users
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import os
import sys
import threading

class TheaterAuftaktGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Theater Auftakt - Audio Processing Tools")
        self.root.geometry("800x700")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs for each script
        self.create_flatten_tab()
        self.create_convert_tab()
        self.create_concatenate_tab()
        self.create_generate_cards_tab()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_flatten_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Flatten Folder")
        
        ttk.Label(frame, text="Flatten Folder", font=("Arial", 16, "bold")).pack(pady=10)
        ttk.Label(frame, text="Flattens nested directories into a single folder with normalized names", 
                 wraplength=600).pack(pady=5)
        
        # Source folder
        ttk.Label(frame, text="Source Folder:").pack(anchor=tk.W, padx=20, pady=(20, 5))
        source_frame = ttk.Frame(frame)
        source_frame.pack(fill=tk.X, padx=20, pady=5)
        self.flatten_source = tk.StringVar()
        ttk.Entry(source_frame, textvariable=self.flatten_source, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(source_frame, text="Browse...", command=lambda: self.browse_folder(self.flatten_source)).pack(side=tk.LEFT, padx=5)
        
        # Dest folder
        ttk.Label(frame, text="Destination Folder:").pack(anchor=tk.W, padx=20, pady=(20, 5))
        dest_frame = ttk.Frame(frame)
        dest_frame.pack(fill=tk.X, padx=20, pady=5)
        self.flatten_dest = tk.StringVar()
        ttk.Entry(dest_frame, textvariable=self.flatten_dest, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(dest_frame, text="Browse...", command=lambda: self.browse_folder(self.flatten_dest)).pack(side=tk.LEFT, padx=5)
        
        # Execute button
        ttk.Button(frame, text="Flatten Folder", command=self.run_flatten).pack(pady=20)
    
    def create_convert_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Convert Audio")
        
        ttk.Label(frame, text="Convert Audio", font=("Arial", 16, "bold")).pack(pady=10)
        ttk.Label(frame, text="Converts M4A files to MP3 format (requires ffmpeg)", 
                 wraplength=600).pack(pady=5)
        
        # Source folder
        ttk.Label(frame, text="Source Folder:").pack(anchor=tk.W, padx=20, pady=(20, 5))
        source_frame = ttk.Frame(frame)
        source_frame.pack(fill=tk.X, padx=20, pady=5)
        self.convert_source = tk.StringVar()
        ttk.Entry(source_frame, textvariable=self.convert_source, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(source_frame, text="Browse...", command=lambda: self.browse_folder(self.convert_source)).pack(side=tk.LEFT, padx=5)
        
        # Dest folder
        ttk.Label(frame, text="Destination Folder:").pack(anchor=tk.W, padx=20, pady=(20, 5))
        dest_frame = ttk.Frame(frame)
        dest_frame.pack(fill=tk.X, padx=20, pady=5)
        self.convert_dest = tk.StringVar()
        ttk.Entry(dest_frame, textvariable=self.convert_dest, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(dest_frame, text="Browse...", command=lambda: self.browse_folder(self.convert_dest)).pack(side=tk.LEFT, padx=5)
        
        # Execute button
        ttk.Button(frame, text="Convert Audio", command=self.run_convert).pack(pady=20)
    
    def create_concatenate_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Concatenate Audio")
        
        ttk.Label(frame, text="Concatenate Audio", font=("Arial", 16, "bold")).pack(pady=10)
        ttk.Label(frame, text="Combines all M4A files from subdirectories into a single file", 
                 wraplength=600).pack(pady=5)
        
        # Source folder
        ttk.Label(frame, text="Source Folder:").pack(anchor=tk.W, padx=20, pady=(20, 5))
        source_frame = ttk.Frame(frame)
        source_frame.pack(fill=tk.X, padx=20, pady=5)
        self.concat_source = tk.StringVar()
        ttk.Entry(source_frame, textvariable=self.concat_source, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(source_frame, text="Browse...", command=lambda: self.browse_folder(self.concat_source)).pack(side=tk.LEFT, padx=5)
        
        # Output file
        ttk.Label(frame, text="Output File:").pack(anchor=tk.W, padx=20, pady=(20, 5))
        output_frame = ttk.Frame(frame)
        output_frame.pack(fill=tk.X, padx=20, pady=5)
        self.concat_output = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.concat_output, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(output_frame, text="Browse...", command=lambda: self.browse_file(self.concat_output)).pack(side=tk.LEFT, padx=5)
        
        # Execute button
        ttk.Button(frame, text="Concatenate Audio", command=self.run_concatenate).pack(pady=20)
    
    def create_generate_cards_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Generate Cards")
        
        ttk.Label(frame, text="Generate Cards", font=("Arial", 16, "bold")).pack(pady=10)
        ttk.Label(frame, text="Creates card-based structure with meta files from audio files", 
                 wraplength=600).pack(pady=5)
        
        # Input folder
        ttk.Label(frame, text="Input Folder:").pack(anchor=tk.W, padx=20, pady=(20, 5))
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, padx=20, pady=5)
        self.cards_input = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.cards_input, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(input_frame, text="Browse...", command=lambda: self.browse_folder(self.cards_input)).pack(side=tk.LEFT, padx=5)
        
        # Output folder
        ttk.Label(frame, text="Output Folder:").pack(anchor=tk.W, padx=20, pady=(20, 5))
        output_frame = ttk.Frame(frame)
        output_frame.pack(fill=tk.X, padx=20, pady=5)
        self.cards_output = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.cards_output, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(output_frame, text="Browse...", command=lambda: self.browse_folder(self.cards_output)).pack(side=tk.LEFT, padx=5)
        
        # Zip option
        self.create_zip = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame, text="Create zip file", variable=self.create_zip).pack(pady=10)
        
        # Execute button
        ttk.Button(frame, text="Generate Cards", command=self.run_generate_cards).pack(pady=20)
    
    def browse_folder(self, var):
        folder = filedialog.askdirectory()
        if folder:
            var.set(folder)
    
    def browse_file(self, var):
        file = filedialog.asksaveasfilename(
            defaultextension=".m4a",
            filetypes=[("M4A files", "*.m4a"), ("All files", "*.*")]
        )
        if file:
            var.set(file)
    
    def run_script(self, script_name, args):
        """Run a script in a separate thread and show output"""
        def run():
            try:
                self.status_var.set(f"Running {script_name}...")
                script_path = os.path.join(os.path.dirname(__file__), script_name)
                
                cmd = [sys.executable, script_path] + args
                result = subprocess.run(cmd, capture_output=True, text=True, check=False)
                
                if result.returncode == 0:
                    self.status_var.set(f"{script_name} completed successfully!")
                    messagebox.showinfo("Success", f"{script_name} completed successfully!")
                else:
                    self.status_var.set(f"{script_name} failed")
                    messagebox.showerror("Error", f"{script_name} failed:\n{result.stderr}")
            except Exception as e:
                self.status_var.set(f"Error: {str(e)}")
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        threading.Thread(target=run, daemon=True).start()
    
    def run_flatten(self):
        source = self.flatten_source.get()
        dest = self.flatten_dest.get()
        if not source or not dest:
            messagebox.showwarning("Missing Input", "Please select both source and destination folders")
            return
        self.run_script("flatten-folder.py", [source, dest])
    
    def run_convert(self):
        source = self.convert_source.get()
        dest = self.convert_dest.get()
        if not source or not dest:
            messagebox.showwarning("Missing Input", "Please select both source and destination folders")
            return
        self.run_script("convert-audio.py", [source, dest])
    
    def run_concatenate(self):
        source = self.concat_source.get()
        output = self.concat_output.get()
        if not source or not output:
            messagebox.showwarning("Missing Input", "Please select source folder and output file")
            return
        self.run_script("concatenate-audio.py", [source, output])
    
    def run_generate_cards(self):
        input_folder = self.cards_input.get()
        output_folder = self.cards_output.get()
        if not input_folder or not output_folder:
            messagebox.showwarning("Missing Input", "Please select both input and output folders")
            return
        args = [input_folder, output_folder]
        if not self.create_zip.get():
            args.append("--no-zip")
        self.run_script("generate-cards.py", args)

if __name__ == "__main__":
    root = tk.Tk()
    app = TheaterAuftaktGUI(root)
    root.mainloop()
