import os
import shutil
from pathlib import Path
# Define the directory you want to clean up
TRACKED_DIR = Path.home() / "OneDrive" / "Desktop" / "test"
# Define your destination folders based on file types
DEST_FOLDERS = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".ppt"],  # Added .pptx / .ppt for your presentations
    "Archives": [".zip", ".tar", ".gz", ".rar"],
    "Applications": [".exe", ".dmg", ".pkg", ".deb", ".msi"],        # Added .msi for installers
}


def organize_folder():
    # 1. Ensure the tracked directory exists
    if not TRACKED_DIR.exists():
        print(f"Directory {TRACKED_DIR} does not exist.")
        return

    # 2. Loop through all items in the folder
    for item in TRACKED_DIR.iterdir():
        # Skip directories, we only want to move files
        if item.is_dir():
            continue

        file_extension = item.suffix.lower()
        moved = False

        # 3. Check which category the file belongs to
        for folder_name, extensions in DEST_FOLDERS.items():
            if file_extension in extensions:
                target_folder = TRACKED_DIR / folder_name

                # Create the category folder if it doesn't exist yet
                target_folder.mkdir(exist_ok=True)

                # Move the file safely
                try:
                    shutil.move(str(item), str(target_folder / item.name))
                    print(f"Moved: {item.name} -> {folder_name}/")
                except Exception as e:
                    print(f"Could not move {item.name}: {e}")

                moved = True
                break

        # Optional: Move unknown files to an "Others" folder
        if not moved and file_extension != "":
            other_folder = TRACKED_DIR / "Others"
            other_folder.mkdir(exist_ok=True)
            try:
                shutil.move(str(item), str(other_folder / item.name))
                print(f"Moved: {item.name} -> Others/")
            except Exception as e:
                print(f"Could not move {item.name}: {e}")


if __name__ == "__main__":
    print("Starting file organization...")
    organize_folder()
    print("Organization complete!")