import shutil  # Import shutil for file operations like copying files.
import os  # Import os for interacting with the file system.
from functions.validate_functions import (
    get_valid_id, get_valid_float, get_valid_int, 
    get_valid_text, get_valid_frequency, get_valid_date
)

def backup_database():
    try:
        # Define the source path for the database file to be backed up.
        source = 'database/finance_dashboard.db'

        # Define the folder where the backup will be stored.
        backup_folder = 'database/backups/'
        os.makedirs(backup_folder, exist_ok=True)  # Create the backup folder if it doesn't exist.

        # Define the full path for the backup file.
        backup_file = os.path.join(backup_folder, 'finance_dashboard_backup.db')

        # Copy the database file to the backup location.
        shutil.copy(source, backup_file)

        # Confirm that the backup was successful.
        print(f"Backup successful! Backup file saved at: {backup_file}")
    except Exception as e:
        # Handle and print any errors that occur during the backup process.
        print(f"Error creating backup: {e}")

def restore_database():
    try:
        # Define the folder and file path for the backup.
        backup_folder = 'database/backups/'
        backup_file = os.path.join(backup_folder, 'finance_dashboard_backup.db')

        # Define the destination path for restoring the database.
        destination = 'database/finance_dashboard.db'

        # Check if the backup file exists before attempting to restore.
        if not os.path.exists(backup_file):
            # Inform the user if no backup file is found.
            print("No backup file found. Please create a backup first.")
            return

        # Copy the backup file to the original database location.
        shutil.copy(backup_file, destination)

        # Confirm that the restore operation was successful.
        print("Restore successful! The database has been restored from the backup.")
    except Exception as e:
        # Handle and print any errors that occur during the restore process.
        print(f"Error restoring database: {e}")
