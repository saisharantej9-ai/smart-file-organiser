import os
import shutil
from pathlib import Path

# Define your destination folders based on file types
DEST_FOLDERS = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".ppt"],
    "Archives": [".zip", ".tar", ".gz", ".rar"],
    "Applications": [".exe", ".dmg", ".pkg", ".deb", ".msi"],
}


def organize_folder(target_path_str):
    # Convert the string input into a Path object and strip accidental wrapper quotes
    tracked_dir = Path(target_path_str.strip('"').strip("'"))

    # 1. Ensure the directory exists
    if not tracked_dir.exists():
        print(f"\n Error: The directory '{tracked_dir}' does not exist. Please check the path and try again.")
        return

    print(f"\nScanning: {tracked_dir}...")
    files_moved = 0

    # 2. Loop through all items in the folder
    for item in tracked_dir.iterdir():
        # Skip directories, we only want to move files
        if item.is_dir():
            continue

        file_extension = item.suffix.lower()
        moved = False

        # 3. Check which category the file belongs to
        for folder_name, extensions in DEST_FOLDERS.items():
            if file_extension in extensions:
                target_folder = tracked_dir / folder_name
                target_folder.mkdir(exist_ok=True)

                try:
                    shutil.move(str(item), str(target_folder / item.name))
                    print(f"Moved: {item.name} -> {folder_name}/")
                    files_moved += 1
                except Exception as e:
                    print(f"Could not move {item.name}: {e}")

                moved = True
                break

        # Move unknown files to an "Others" folder
        if not moved and file_extension != "":
            code_folder = tracked_dir / "Code"
            code_folder.mkdir(exist_ok=True)
            try:
                shutil.move(str(item), str(code_folder / item.name))
                print(f"Moved: {item.name} -> Code/")
                files_moved += 1
            except Exception as e:
                print(f"Could not move {item.name}: {e}")
    print(f"\n Organization complete! Total files moved: {files_moved}")


if __name__ == "__main__":
    print("=== Smart File Organizer ===")
    # Prompt the user to paste their path directly
    user_input = input("Paste the absolute path of the folder you want to organize: ")
    organize_folder(user_input)