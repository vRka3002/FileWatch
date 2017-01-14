"""
    File to handle the events generated while making changes in stock file
"""

import sys
import time
from globals import Global
from products import Products
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class ChangeHandler(PatternMatchingEventHandler):
    """
        Class to handle events of file changes(modify, created etc.)
    """

    def on_modified(self, event):
        """
            Function to call for modification in product holder
        :param event: Type of event
        :return: Changed product container
        """
        Products.create_product_holder(Global.csvPath)

    @staticmethod
    def initiate_file_monitoring(filepath):
        """
            Function to start the file monitoring
        :rtype: File handler
        :param filepath: Path where the file is located
        :return: Creates a instance for observing the file
        """
        Global.observer = Observer()
        Global.observer.schedule(ChangeHandler(), path=filepath)
        Global.observer.start()
        print "Watching File"

    @staticmethod
    def stop_file_monitoring():
        """
            Function to stop the monitoring of file by closing the socket
        :return: None
        """
        Global.observer.stop()
        Global.observer.join()


# Driver function
if __name__ == '__main__':
    args = sys.argv[1:]  # Get path of the file
    file_location = args[0] if args else '.'  # Store path of file
    Global.csvPath = args[1]
    # Initiate file monitoring
    ChangeHandler.initiate_file_monitoring(file_location)
    # Form holder containing data
    Products.create_product_holder(Global.csvPath)

    try:
        while True:
            # Print User Options
            print "Select Operation: "
            print "1. Get max data"
            print "2. Get min data"
            print "3. Get max data"
            print "Ctrl+z to exit"
            userInput = raw_input()
            # Iterate over user input
            if userInput == '1':
                values = Products.fetch_max_values()  # Extract minimum values
                Products.print_data(values)  # Print the values
            elif userInput == '2':
                values = Products.fetch_min_values()    # Extract minimum values
                Products.print_data(values)     # Print the values
            elif userInput == '3':
                codes = raw_input("Enter Product Codes Seperated By Space - ")
                values = Products.get_specific_min_price(codes.split())     # Extract data for products
                Products.print_data(values)
            else:
                print "Choose correct option"
    except KeyboardInterrupt:
        ChangeHandler.stop_file_monitoring()

    print "Good Luck Finding Data On Your Own -_-"
