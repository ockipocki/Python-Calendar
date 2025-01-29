"""
Title: the_calendar.py
Author: Oskar Bergström
Date: 2022-04-10
"""

import datetime
from os import listdir, mkdir, getcwd
from os.path import join
from shutil import rmtree


class Activity:
    """
    Attributes:
    start_time: The start time of the activity
    end_time: The end time of the activity
    event: The activity event
    """
    def __init__(self, start_time, end_time, event):
        """
        Used when creating a new activity object
        :param start_time: A string, time in the format HH:MM, ex: 14:30
        :param end_time: A string, time in the same format as start_time
        :param event: A string, the event that takes place during the time interval
        """
        self.start_time = start_time
        self.end_time = end_time
        self.event = event

    def __str__(self):
        """
        Creates a string representation of the activity object.
        :return: A string, example: 10:00-11:30: Book club
        """
        return self.start_time + "-" + self.end_time + ": " + self.event

    def __lt__(self, other):
        """
        Less-than-comparison of two activity objects. Makes a string comparison between their start_time attributes.
        Used when sorting lists of activity objects.
        :param other: Another activity object
        :return: A boolean
        """
        if self.start_time < other.start_time:
            return True
        else:
            return False

    def change_start_time(self, new_time):
        """
        Sets new value for the activity start time
        :param new_time: string -- the new time value
        :return: (nothing)
        """
        self.start_time = new_time

    def change_end_time(self, new_time):
        """
        Sets new value for the activity end time
        :param new_time: string -- the new time value
        :return: (nothing)
        """
        self.end_time = new_time

    def change_event(self, new_event):
        """
        Sets new value for the activity event
        :param new_event: string -- the new event value
        :return:
        """
        self.event = new_event


class Page:
    """
    Attributes:
    date: The date for the calendar page
    activities: The activities planned for that date
    """
    def __init__(self, date, activities=None):
        """
        Called whenever a new page object is created
        :param date: A datetime.date() object, represents the date for the calendar page
        :param activities: A list of activity objects. Empty list if no activities argument is given.
        """
        if activities is None:
            activities = []
        self.date = date
        self.activities = activities

    def __str__(self):
        """
        Used for representing pages as strings. Checks if there are no activities to display.
        :return: A string including the page date and activities.
        Ex:
        Date: 2022-04-10:
        Activities
        10:00-11:00 Book club meeting
        """
        page_string = "Datum: " + str(self.date) + "\n"
        if not self.activities:
            page_string += "(Inga aktiviteter för dagen)"
        else:
            page_string += "Aktiviteter"
            for activity in self.activities:
                page_string += ("\n" + str(activity))

        return page_string

    def __lt__(self, other):
        """
        Less-than-or-equal comparison of page objects, by date attribute. Used when sorting list of pages
        :param other: other page object to compare with
        :return: A boolean value, resulting from the comparison
        """
        return self.date < other.date

    def get_start_end_times(self):
        while True:
            start_time = get_time_input("Ange starttid för aktiviteten (HHMM): ")
            while True:
                end_time = get_time_input("Ange sluttid för aktiviteten (HHMM): ")
                if end_time <= start_time:
                    print("Sluttiden kan inte vara innan eller lika med starttiden för aktiviteten!")
                else:
                    break
            if self.overlapping_times(start_time, end_time):
                answer = get_yes_no_input("Tiden överlappar med en annan aktivitet! Vill du lägga till ändå? (j/n): ")
                if answer == "yes":
                    return start_time, end_time
            else:
                return start_time, end_time

    def add_activity(self):
        """
        Creates and adds a new activity to the page.activities list
        :return: (nothing)
        """
        print("----Lägg till ny aktivitet----")
        (start_time, end_time) = self.get_start_end_times()
        event = input("Ange aktivitet: ")
        activity = Activity(start_time, end_time, event)
        self.activities.append(activity)
        self.activities.sort()

    def choose_activity(self):
        """
        Used to let the user choose an activity from page.activities which is then returned.
        :return: activity object -- the chosen activity. None if there are no activities to choose from.
        """
        # If there are no activities to choose from
        if not self.activities:
            print("Det finns inga aktiviteter!")
            return
        # Return activity if there's only one activity in list
        if len(self.activities) == 1:
            return self.activities[0]
        else:
            # Create a numbered list of the activities, but prefixed with a numbering starting at 1
            activity_options = []
            for i in range(len(self.activities)):
                activity_options.append("(" + str(i + 1) + ") " + str(self.activities[i]))
            # Print out options and get user choice
            display_options(activity_options)
            choice = get_choice_input(activity_options)
            # Chosen activity is at index choice - 1
            chosen_activity_index = choice - 1
            return self.activities[chosen_activity_index]

    def remove_activity(self):
        """
        Removes an activity, specified by the user, from page.activities
        :return:
        """
        print("----Ta bort aktivitet----")
        chosen_activity = self.choose_activity()
        self.activities.remove(chosen_activity)

    def execute_activity_option(self, option, chosen_activity):
        """
        Makes changes to the chosen activity, depending on the chosen option
        :param option: int --- 1 to 3, the option chosen
        :param chosen_activity: activity object -- the activity to make changes to
        :return:
        """
        if option == 1:
            print("----Ändra starttid----")
            activity_end_time = chosen_activity.end_time
            while True:
                new_start_time = get_time_input("Ange ny starttid för aktiviteten (HHMM): ")
                # Check if times overlap
                if self.overlapping_times(new_start_time, activity_end_time):
                    print("Tiden överlappar med en annan aktivitet!")
                    answer = get_yes_no_input("Vill du ändra tiden ändå? (j/n): ")
                    if answer == "yes":
                        chosen_activity.change_start_time(new_start_time)
                        return
        elif option == 2:
            print("----Ändra sluttid----")
            activity_start_time = chosen_activity.start_time
            while True:
                new_end_time = get_time_input("Ange ny sluttid för aktiviteten (HHMM): ")
                # Check if times overlap
                if self.overlapping_times(activity_start_time, new_end_time):
                    print("Tiden överlappar med en annan aktivitet!")
                    answer = get_yes_no_input("Vill du ändra tiden ändå? (j/n): ")
                    if answer == "yes":
                        chosen_activity.change_end_time(new_end_time)
                        return
        elif option == 3:
            print("----Ändra aktiviteten----")
            event = input("Ange aktivitet: ")
            chosen_activity.change_event(event)

    def change_activity(self):
        """
        Used to let the user choose an activity from page.activities and change its start time, end time or event.
        :return:
        """
        # User picks which activity to change
        chosen_activity = self.choose_activity()
        if chosen_activity is None:
            return
        # Activity has been picked
        print("----Ändra aktivitet----")
        print("Vad vill du ändra?")
        print("Aktivitet: " + str(chosen_activity))
        # User picks what they would like to change
        activity_options = ["1. Aktivitetens starttid", "2. Aktivitetens sluttid", "3. Aktiviteten"]
        display_options(activity_options)
        choice = get_choice_input(activity_options)
        # Execute choice
        self.execute_activity_option(choice, chosen_activity)

    def overlapping_times(self, start_time, end_time):
        """
        Checks if start and end times overlap with any of the activities
        :param start_time: string -- start time to
        :param end_time: string -- end time
        :return:
        """
        for activity in self.activities:
            cond1 = activity.start_time <= start_time < activity.end_time
            cond2 = activity.start_time < end_time <= activity.end_time
            cond3 = start_time < activity.start_time and end_time > activity.end_time
            if cond1 or cond2 or cond3:
                return True

        return False


class Calendar:
    """
    Attributes:
    storage_format: int, 1 or 2, representing the chosen storage
    pages: list of page objects that make up the calendar
    current_page_index: index used to keep track of current page
    data_folder_path: path to folder for storing data files
    data_file_path: path to/name of file for storing data
    """
    def __init__(self, storage_format, pages=None, current_page_index=0,
                 data_folder_path=join(getcwd(), "pages"), data_file_path="pages.txt"):

        self.storage_format = storage_format
        self.pages = pages
        self.current_page_index = current_page_index
        self.data_folder_path = data_folder_path
        self.data_file_path = data_file_path

    def load_pages(self):
        """
        Read pages from data file or data folder, depending on the calendar storage format.
        Creates and adds a new page to the calendar if there is no data.
        :return: (nothing)
        """
        if self.storage_format == 1:
            self.pages = read_pages_from_file(self.data_file_path)
        elif self.storage_format == 2:
            self.pages = read_pages_from_folder(self.data_folder_path)

        if not self.pages:
            print("Kunde inte hitta någon tidigare data!")
            self.add_page()

    def save_pages(self):
        """
        Writes pages to data file or data folder, depending on the calendar storage format.
        :return: (nothing)
        """
        if self.storage_format == 1:
            write_pages_to_file(self.pages, self.data_file_path)
        elif self.storage_format == 2:
            write_pages_to_folder(self.pages, self.data_folder_path)

    def add_page(self):
        """
        Lets the user create and add a new page to the calendar.
        :return: (nothing)
        """
        print("----Lägg till ny sida i kalendern----")
        # Gets page date from user, checks that there are no other pages with same date
        while True:
            date = get_date_input()
            if any(date == page.date for page in self.pages):
                print("Det finns redan en sida med datumet " + str(date) + "!")
            else:
                break

        page = Page(date)           # Create page with empty activity lsit
        page.add_activity()         # Add activity to page
        self.pages.append(page)     # Add page to calendar pages
        self.pages.sort()           # Sort by page date

    def delete_current_page(self):
        """
        Deletes the currently displayed page from calendar page list
        :return: (nothing)
        """
        del self.pages[self.current_page_index]     # Delete page at current index
        # If calendar page list is empty, create and add new page
        if not self.pages:
            self.add_page()
        # If current page index is out of bounds after deleting page, move the index back one element
        if self.current_page_index >= len(self.pages):
            self.current_page_index -= 1

    def display_all_pages(self):
        """
        Used to print out all pages in the calendar page list
        :return: (nothing)
        """
        print("----Alla sidor----")
        for page in self.pages:
            print(page)

    def display_activities_this_month(self):
        """
        Used to display all activities with the same year and month as today's date
        :return: (nothing)
        """
        current_date = datetime.datetime.today().date()     # Today's date
        print("----Aktiviteter för den här månaden----")
        activities_this_month = []
        # Print activities with same year and month as today' date
        for page in self.pages:
            if page.date.year == current_date.year and page.date.month == current_date.month:
                print(page)
                activities_this_month.append(page)
        # If list is empty, there are no activities for this month
        if not activities_this_month:
            print("Inga aktiviteter den här månaden")

    def change_current_page(self, number_of_pages):
        """
        Used to change the current page index for when browsing through the calendar pages.
        Index wraps around page list.
        :param number_of_pages: int -- the number of pages to browse by
        :return: (nothing)
        """
        self.current_page_index = (self.current_page_index + number_of_pages) % len(self.pages)

    def execute_option(self, option):
        """
        Called to execute the different menu options.
        :param option: int -- the option to be executed
        :return: (nothing)
        """
        if option == 1:                                             # Go forward one page
            self.change_current_page(1)
        elif option == 2:                                           # Go back one page
            self.change_current_page(-1)
        elif option == 3:                                           # Add new page to calendar
            self.add_page()
        elif option == 4:                                           # Delete the current page
            self.delete_current_page()
        elif option == 5:                                           # Show all calendar pages
            self.display_all_pages()
        elif option == 6:                                           # Add activity to current page
            self.pages[self.current_page_index].add_activity()
        elif option == 7:                                           # Remove activity from current page
            self.pages[self.current_page_index].remove_activity()
        elif option == 8:                                           # Change activity on current page
            self.pages[self.current_page_index].change_activity()
        elif option == 9:                                           # Show all activities this month
            self.display_activities_this_month()
        elif option == 10:                                          # Save date and quit the program
            self.save_pages()
            quit()


def get_yes_no_input(prompt_string):
    """"
    Used to get a yes or no input from the user
    :param prompt_string: string -- the input prompt shown to user
    :return: string -- "yes" or "no", depending on if they answered yes or no
    """
    while True:
        answer = input(prompt_string).lower()   # Make input lowercase, in case input happens to be uppercase
        if answer == "j":
            return "yes"
        elif answer == "n":
            return "no"
        else:
            print("Inte giltigt svar, ange j eller n!")


def get_int_input(prompt_string):
    """
    Used to get an int from user input, handles ValueError exception.
    :param prompt_string: a string, the input prompt shown to the user
    :return: the int that was asked for
    """
    while True:
        try:
            return int(input(prompt_string))
        except ValueError:
            print("Ange ett tal!")


def get_choice_input(options):
    """
    Gets a choice input from the user when they're presented with options. Checks that the option they chose is valid
    :param options: A list of strings, the options presented to the user
    :return: choice: An int, the option they chose
    """
    while True:
        choice = get_int_input("Ange ett heltal: ")
        number_of_options = len(options)
        if choice in range(1, number_of_options + 1):
            return choice
        else:
            print(choice, "är inte att valbart alternativ!")


def display_options(options):
    """
    Prints options given as a list of strings
    :param options: A list of strings, the options
    :return: (nothing)
    """
    for option in options:
        print(option)


def get_storage_format():
    """
    Used to get input from user for their preferred method of storage.
    :return storage_format: An int (1 or 2), 1 = single file, 2 = files in folder
    """
    storage_options = ["1. All data sparas i en och samma fil",
                       "2. Data sparas i flera filer, där varje fil motsvarar en sida ur kalendern"]
    # Print storage options
    print("Hur vill du läsa in/lagra din data?")
    display_options(storage_options)
    # Get user input
    storage_format = get_choice_input(storage_options)
    return storage_format


def read_pages_from_folder(folder_path):
    """
    Used for reading page data when the storage format is one page per file
    :param folder_path: A string, the path to the data folder directory
    :return: A list of page objects, the calendar pages. Empty if there's no data or if there are no files.
    """
    pages = []                                                  # Empty list for page objects
    try:
        folder_files = listdir(folder_path)                     # List of file names in folder
        for file_name in folder_files:
            file_path = join(folder_path, file_name)            # File path for file in folder
            fob = open(file_path, "r", encoding="utf-8")        # Open file at file path
            page = create_page_from_line(fob.readline())        # Read first line, create a page
            pages.append(page)                                  # Add page to list
            fob.close()
    except FileNotFoundError:
        pass

    return pages


def create_page_from_line(line):
    """
    Used to create a page object from a line in csv-file
    :param line: A string, the line containing data in csv-format for creating a page object
    :return: A page object, created from data contained in line
    """
    page_data = line.strip().split(";")     # Strip string and make list of page data
    date = datetime.datetime.strptime(page_data[0], "%Y-%m-%d").date()     # First field contains the page date
    if len(page_data) == 1:
        return Page(date)
    else:
        activities = []  # Empty list for activity objects
        for i in range(1, len(page_data), 3):                           # For each activity data set
            start_time = page_data[i]
            end_time = page_data[i + 1]
            event = page_data[i + 2]
            activities.append(Activity(start_time, end_time, event))    # Create activity object and add to list

        return Page(date, activities)   # Create the page object


def read_pages_from_file(file_name):
    """
    Used to get the calendar page objects from a file and return them in a list
    :param file_name: string -- for the name of the file to read from
    :return: list of page objects -- The pages read from the file
    """
    pages = []
    try:
        # Open file to read
        fob = open(file_name, "r", encoding="utf-8")
        # Read page objects and add to list
        for line in fob.readlines():
            page = create_page_from_line(line)
            pages.append(page)
        fob.close()
    except FileNotFoundError:
        pass

    return pages


def write_pages_to_file(pages, file_name):
    """
    Writes pages to a file.
    :param pages: list of page objects -- The list containing the calendar pages
    :param file_name: string -- the name of the file to write to
    :return: (nothing)
    """
    # Open the file in write mode
    fob = open(file_name, "w", encoding="utf-8")
    # For every page object, write a line containing date and activities data
    for page in pages:
        fob.write(str(page.date))
        for activity in page.activities:
            fob.write(";" + activity.start_time + ";" + activity.end_time + ";" + activity.event)
        fob.write("\n")
    fob.close()


def write_pages_to_folder(pages, folder_path):
    """
    Takes a list of page objects and writes their data to a folder of csv-files.
    :param folder_path: string -- the path to the data folder
    :param pages: list of page objects -- the pages to be written
    :return: (nothing)
    """
    # Create new data folder or overwrite previous folder if folder already exists
    try:
        mkdir(folder_path)      # Make data folder
    except FileExistsError:
        rmtree(folder_path)     # Remove folder and contents
        mkdir(folder_path)
    # For every page, create a file in the folder and write data to it
    for page in pages:
        filename = str(page.date) + ".txt"                  # Create a unique file name, using page date
        file_path = join(folder_path, filename)             # Make file path in folder
        fob = open(file_path, "w", encoding="utf-8")
        # Write page to file
        fob.write(str(page.date))
        for activity in page.activities:
            fob.write(";" + activity.start_time + ";" + activity.end_time + ";" + activity.event)
        fob.close()


def get_date_input():
    """
    Used to get datetime.date() object from user input. Checks if date exists.
    :return: datetime.date() object -- the date from user input
    """
    while True:
        try:
            date_input = input("Ange datum (ÅÅÅÅMMDD): ")
            date = datetime.datetime.strptime(date_input, "%Y%m%d").date()  # Create datetime.datetime object
            return date
        except ValueError:
            print("Ej ett giltigt datum!")                                  # Error if datetime object can't be created


def get_time_input(prompt_string):
    """
    Returns time input from user if the time is valid.
    :param prompt_string: string -- prompt given to the user
    :return: string -- the time
    """
    while True:
        # User inputs time
        time_string = input(prompt_string)
        # Check that the time input is valid (can be turned into a datetime object) for different formats
        time_formats = ["%H%M", "%H:%M", "%H.%M", "%H %M"]
        for time_format in time_formats:
            try:
                # Try to create datetime object
                dto = datetime.datetime.strptime(time_string, time_format)
                # Return the time as a string in the format HH:MM
                return dto.strftime("%H:%M")
            except ValueError:
                pass

        # If none of the delimiters worked, time input must be invalid.
        print("Ej en giltig tid!")


def initialize_calendar():
    """
    Creates and setups a calendar object
    :return: calendar, the created calendar object
    """
    # Welcome message
    print("Välkommen till kalendern!")
    # Get preferred storage format from user
    storage_format = get_storage_format()
    calendar = Calendar(storage_format)
    # Read calendar pages data
    calendar.load_pages()
    return calendar


def menu(menu_options):
    """
    Displays the menu options.
    :param menu_options: List of strings -- the options to be printed.
    :return: (nothing)
    """
    print("----Meny----")
    display_options(menu_options)


def main():
    """
    The main function. Sets up the calendar and goes into the program loop.
    :return: (nothing)
    """
    # Set up the calendar
    calendar = initialize_calendar()

    menu_options = ["1. Bläddra framåt", "2. Bläddra bakåt", "3. Sätt in ny sida",
                    "4. Ta bort sidan", "5. Visa alla sidor", "6. Lägg till aktivitet",
                    "7. Ta bort aktivitet", "8. Ändra aktivitet", "9. Visa månadens aktiviteter", "10. Avsluta"]

    # Program loop until user quits
    while True:
        if not calendar.pages:
            calendar.add_page()
        # Display current page
        print("----Aktuell sida----")
        print(calendar.pages[calendar.current_page_index])
        # Display menu
        menu(menu_options)
        # Get user input
        choice = get_choice_input(menu_options)
        # Execute corresponding option
        calendar.execute_option(choice)


if __name__ == '__main__':
    main()
