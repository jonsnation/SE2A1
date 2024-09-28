CODING COMPETITIONS PLATFORM CLI APPLICATION

The Coding Competitions Platform CLI App is designed to manage and facilitate coding competitions for students. It allows admins (competition hosts) to create competitions and import results for the created competition, by specifying an admin ID, while students can view the list of competitions and their results. The application is built using Python FlaskMVC and SQLAlchemy.

FEATURES

Admin Functions:
Create competitions
Import competition results from CSV files
View list of competitions
View results for specific competitions and users

Student Functions:
View list of competitions
View results for specific competitions and users

CLI COMMANDS FOR FLASK APPLICATION

INITIALIZE DATABASE
Command: flask init
Description: Creates and initializes the database.


USER COMMANDS
Command Group: user
Description: Commands related to user operations.
Create User Command: user create
Description: Creates a new user.
Usage:
flask user create <username> <password> <role>

Example:
flask user create jon jonpass admin

(An admin must be created in order to test the create competitions command and import results command. This is because both  commands require admin privileges, and the admin ID is used as  a parameter in these commands. This creates a form of authority between the  admin and the student.)


LIST USERS
Command: user list
Description: Lists all users in the database.
Usage:
flask user list <format>

Example:
flask user list string

COMPETITION COMMANDS
Command Group: competition
Description: Commands related to competition operations.

Create Competition Command: competition create
Description: Creates a new competition.

Usage:
flask competition create <name> --description <description> --date <date> --admin-id <admin_id>
Example:
flask competition create "HackerRank" --description "Year 3's" --date 2024-09-30 --admin-id 2

LIST COMPETITIONS
Command: competition list
Description: Lists all competitions.
Usage:
flask competition list <format>

Example:
flask competition list string

UPDATE COMPETITIONS
Command: competition update
Description: Updates competition details.
Usage:
flask competition update <competition_id> <name> <description> <date>


Example:
flask competition update 1 "New Name" "New Description" 2024-10-01

RESULT COMMANDS
Command Group: result
Description: Commands related to result operations.

ADD RESULT
Command: result add
Description: Adds a result to a competition for a student.
Usage:
flask result add <competition_id> <user_id> <score> <rank> <time_taken> <problems_solved>

Example:
flask result add 1 2 95 1 3600 5

LIST RESULTS BY COMPETITION
Command: result list_by_competition
Description: Lists all results for a competition.
Usage:
flask result list_by_competition <competition_id>

Example:
flask result list_by_competition 1

LIST RESULTS BY USER
Command: result list_by_user
Description: Lists all results for a user.
Usage:
flask result list_by_user <user_id>

Example:
flask result list_by_user 2

TEST COMMANDS
Command Group: test
Description: Commands related to testing.

RUN USER TESTS
Command: test user
Description: Runs user tests.
Usage:
flask test user <type>

Example:
flask test user unit

