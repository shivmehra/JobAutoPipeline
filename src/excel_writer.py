# Excel writer
import os
import pandas as pd

class ExcelWriter:
    def __init__(self, file_path, sheet_name='Sheet1'):
        self.file_path = file_path
        self.sheet_name = sheet_name

        # Ensure the directory exists
        dir_path = os.path.dirname(file_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        else:
            print("Warning: No directory specified for Excel file.")

    def write_data(self, data, worksheet_name=None):
        """Write data to Excel file"""
        try:
            if not data:
                print("No data to write")
                return False

            # Use provided worksheet_name or default
            sheet_name = worksheet_name or self.sheet_name

            # Convert data to DataFrame
            df = pd.DataFrame(data)

            # Write to Excel
            with pd.ExcelWriter(self.file_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)

            print(f"Data written to Excel file: {self.file_path}")
            return True
        except Exception as e:
            print(f"Error writing to Excel file: {e}")
            return False

    def append_data(self, data, worksheet_name=None):
        """Append data to existing Excel file"""
        try:
            if not data:
                print("No data to append")
                return False

            sheet_name = worksheet_name or self.sheet_name

            # Check if file exists
            if os.path.exists(self.file_path):
                # Read existing data
                try:
                    existing_df = pd.read_excel(self.file_path, sheet_name=sheet_name)
                except:
                    # Sheet doesn't exist, create new
                    existing_df = pd.DataFrame()
            else:
                existing_df = pd.DataFrame()

            # Convert new data to DataFrame
            new_df = pd.DataFrame(data)

            # Append new data
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)

            # Write back to Excel
            with pd.ExcelWriter(self.file_path, engine='openpyxl') as writer:
                combined_df.to_excel(writer, sheet_name=sheet_name, index=False)

            print(f"Data appended to Excel file: {self.file_path}")
            return True
        except Exception as e:
            print(f"Error appending to Excel file: {e}")
            return False