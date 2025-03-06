# ------------------------------------------------------------------------------------------ #
# Title: Assignment06_Starter
# Desc: This assignment demonstrates using functions
# with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   MYoung,3/5/2025,Updated script to include function, classes, and use a
#                          separation of concerns pattern
# ------------------------------------------------------------------------------------------ #
import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
# Define the Data Constants
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables and constants
menu_choice: str  # Hold the choice made by the user.
students: list = []  # a table of student data

# Data Storage
class FileProcessor:
    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        '''
        This function reads the student data from the file and stores it into a table of dictionaries.

        ChangeLog: (Who, When, What)
        MYoung, 3/5/2025, Function Creation

        :param file_name: string of file name to be read
        :param student_data: table that student data is stored in
        :return: table of student data
        '''

        # When the program starts, read the file data into a list of lists (table)
        # Extract the data from the file
        try:
            file = open(file_name, "r")
            student_data = json.load(file)
            file.close()
        except Exception as e:
            IO.output_error_messages(message="Please check that the file exists and that it is in a json format.", error=e)
        except FileNotFoundError as e:
            IO.output_error_messages(message="Error: There was a problem with reading the file.", error=e)
        finally:
            if file.closed == False:
                file.close()
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        '''
        This function writes the student data into the file and stores it into a table.

        ChangeLog: (Who, When, What)
        MYoung, 3/5/2025, Function Creation

        :param file_name:  string of file name to be written
        :param student_data: table of student data to be written into the file
        '''

        try:
            file = open(file_name, "w")
            json.dump(students, file, indent="")
            file.close()
            print("The following data was saved to file!")
            IO.output_student_courses(student_data=student_data)
        except Exception as e:
            error_message = "Error: There was a problem with writing to the file."\
                            "\nPlease check that the file is not open by another program."
            IO.output_error_messages(message=error_message, error=e)
        finally:
            if file.closed == False:
                file.close()

# Presentation Layer
class IO:
    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        '''
        This function outputs error messages when an error occurs.

        ChangeLog: (Who, When, What)
        MYoung, 3/5/2025, Function Creation

        :param message: string of error message to be displayed
        :param error: error type
        '''

        print(message)
        if error is not None:
            # Prints the custom message
            print("-- Technical Error Message -- ")
            print(error.__doc__)
            print(error.__str__())

    @staticmethod
    def output_menu(menu: str):
        '''
        This function displays menu options for the user to choose from.

        ChangeLog: (Who, When, What)
        MYoung, 3/5/2025, Function Creation

        :param menu: string of menu options to be selected from
        '''

        print(menu)

    @staticmethod
    def input_menu_choice():
        '''
        This function collects user choice from menu options

        ChangeLog: (Who, When, What)
        MYoung, 3/5/2025, Function Creation

        :return: string of user's menu choice
        '''

        try:
            choice = input("What would you like to do: ")
            if choice not in ["1", "2", "3", "4"]:
                raise Exception("Please only choose option 1, 2, or 3")
        except Exception as e:
            IO.output_error_messages(message="Please only choose option 1, 2, or 3", error=e)
        return choice

    @staticmethod
    def output_student_courses(student_data: list):
        '''
        This function displays list of registered student data.

        ChangeLog: (Who, When, What)
        MYoung, 3/5/2025, Function Creation

        :param student_data: list of student data to be displayed
        '''

        # Process the data to create and display a custom message
        print("-" * 50)
        for student in student_data:
            print(f'Student {student["FirstName"]} '
                  f'{student["LastName"]} is enrolled in {student["CourseName"]}')
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        '''
        This function collects student data from user input to be stored in a table.

        ChangeLog: (Who, When, What)
        MYoung, 3/5/2025, Function Creation

        :param student_data: list of stored user data
        '''

        student_first_name: str
        student_last_name: str
        course_name: str
        student: dict

        try:
            student_first_name = input("Enter the student's first name: ")
            if not student_first_name.isalpha():
                raise ValueError("The first name should not contain numbers.")
            student_last_name = input("Enter the student's last name: ")
            if not student_last_name.isalpha():
                raise ValueError("The last name should not contain numbers.")
            course_name = input("Please enter the name of the course: ")
            student = {"FirstName": student_first_name,
                        "LastName": student_last_name,
                        "CourseName": course_name}
            student_data.append(student)
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as e:
            IO.output_error_messages(message="Invalid name was entered", error=e)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with your entered data.", error=e)

# Processing Layer
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Present and Process the data
while (True):

    # Present the menu of choices
    IO.output_menu(menu=MENU)
    menu_choice = IO.input_menu_choice()

    # Input user data
    if menu_choice == "1":  # This will not work if it is an integer!
        IO.input_student_data(student_data=students)
        continue

    # Present the current data
    elif menu_choice == "2":
        IO.output_student_courses(student_data=students)
        continue

    # Save the data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    # Stop the loop
    elif menu_choice == "4":
        break  # out of the loop

print("Program Ended")
