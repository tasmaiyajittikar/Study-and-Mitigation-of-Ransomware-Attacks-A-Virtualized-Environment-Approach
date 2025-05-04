import os
import shutil
import subprocess
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import shutil


# Creates pop-up for user to keep directory locked or unlock directory
def ask_to_unlock():
        root = tk.Tk()
        root.withdraw()
        # Create pop-up
        result = messagebox.askyesno("Locked Critical Directory", "Directory locked due to suspicious activity.\nDo you want to unlock it?\nFiles will be backed up to \"./backups\".")
        root.destroy()
        return result


# Locks down directory and prompts user for unlock
def mitigation(watch_path):
        try:
                # Lock down directory
                subprocess.run(["chattr", "-R", "+i", watch_path], check=True)
                backup(watch_path)
        except Exception as e:
                print(f"Failed to lock directory with chattr: {e}")
        # Prompt and alert user
        if ask_to_unlock():
                # Unlock directory if user chooses yes
                subprocess.run(["chattr", "-R", "-i", watch_path], check=True)


# Creates backup of files
def backup(src_dir, backup_root="./backups"):
        try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_dir = os.path.join(backup_root, f"backup_{timestamp}")
                # Creates new directory
                os.makedirs(backup_dir, exist_ok=True)
                # Copies files over to new directory
                shutil.copytree(src_dir, backup_dir, dirs_exist_ok=True)


                return backup_dir
        except Exception as e:
                print(f"Backup failed: {e}")
                return None
