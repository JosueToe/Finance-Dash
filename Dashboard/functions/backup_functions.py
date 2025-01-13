import shutil
import os

def backup_database():
    try:
        # Define source and destination paths
        source = 'database/finance_dashboard.db'
        backup_folder = 'database/backups/'
        os.makedirs(backup_folder, exist_ok=True)
        backup_file = os.path.join(backup_folder, 'finance_dashboard_backup.db')

        # Copy the database file to the backup location
        shutil.copy(source, backup_file)
        print(f"Backup successful! Backup file saved at: {backup_file}")
    except Exception as e:
        print(f"Error creating backup: {e}")


def restore_database():
    try:
        # Define source and destination paths
        backup_folder = 'database/backups/'
        backup_file = os.path.join(backup_folder, 'finance_dashboard_backup.db')
        destination = 'database/finance_dashboard.db'

        # Check if a backup file exists
        if not os.path.exists(backup_file):
            print("No backup file found. Please create a backup first.")
            return

        # Copy the backup file to the original database location
        shutil.copy(backup_file, destination)
        print("Restore successful! The database has been restored from the backup.")
    except Exception as e:
        print(f"Error restoring database: {e}")
