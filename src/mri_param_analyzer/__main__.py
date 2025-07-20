"""Main entry point for MRI Parameter Analyzer."""

import sys
import argparse
from .dashboard.app import app
from .core.database import connect_to_database, create_tables
from .core.dicom_reader import main as process_dicom


def main():
    """Main function to handle CLI arguments."""
    parser = argparse.ArgumentParser(description="MRI Parameter Analyzer")
    parser.add_argument(
        "command",
        choices=["dashboard", "setup-db", "process-dicom"],
        help="Command to run"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Run in debug mode"
    )
    
    args = parser.parse_args()
    
    if args.command == "dashboard":
        print("Starting dashboard...")
        app.run_server(debug=args.debug)
    elif args.command == "setup-db":
        print("Setting up database...")
        conn = connect_to_database()
        if conn:
            create_tables(conn)
        else:
            print("Failed to connect to database")
            sys.exit(1)
    elif args.command == "process-dicom":
        print("Processing DICOM files...")
        process_dicom()


if __name__ == "__main__":
    main() 