# Coding Competitions Platform CLI Application

*The Coding Competitions Platform CLI App is designed to manage and facilitate coding competitions for students. It allows admins (competition hosts) to create competitions and import results for the created competition, by specifying an admin ID, while students can view the list of competitions and their results. The application is built using Python Flask MVC and SQLAlchemy.*

## Features

### Admin Functions:
- Create competitions
- Import competition results from CSV files
- View list of competitions
- View results for specific competitions and users

### Student Functions:
- View list of competitions
- View results for specific competitions and users

## CLI Commands for Flask Application

### Initialize Database
- **Command**: `flask init`
- **Description**: Creates and initializes the database.

### User Commands
- **Command Group**: `user`
- **Description**: Commands related to user operations.
  
- **Create User Command**: 
  - **Command**: `user create`
  - **Description**: Creates a new user.
  - **Usage**: `flask user create <username> <password> <role>`
  - **Example**: `flask user create tanjiro tanjiropass admin`
  
*(An admin must be created in order to test the create competitions command and import results command. This is because both commands require admin privileges, and the admin ID is used as a parameter in these commands. This creates a form of authority between the admin and the student. A message with the ID is produced so that the admin can see their ID to use for creating competitions, and importing resultd for said cometition)*

- **List Users**: 
  - **Command**: `user list`
  - **Description**: Lists all users in the database.
  - **Usage**: `flask user list <format>`
  - **Example**: `flask user list string`

### Competition Commands
- **Command Group**: `competition`
- **Description**: Commands related to competition operations.

*(A competition must be created to successfully import the results that map to the created competition ID from the CSV. In order for a competition to be stored in the database, it must be created by an admin. It is not created via importing since there are no competition names in the CSV file, only IDs. Once a competition ID in the database maps with a competition ID in the CSV file, the results can be imported.)*

- **Create Competition Command**: 
  - **Command**: `competition create`
  - **Description**: Creates a new competition.
  - **Usage**: `flask competition create <name> --description <description> --date <date> --admin-id <admin_id>`
  - **Example**: `flask competition create "HackerRank" --description "Year 3's" --date 2024-09-30 --admin-id 2`

- **List Competitions**: 
  - **Command**: `competition list`
  - **Description**: Lists all competitions.
  - **Usage**: `flask competition list <format>`
  - **Example**: `flask competition list string`

- **Update Competitions**: 
  - **Command**: `competition update`
  - **Description**: Updates competition details.
  - **Usage**: `flask competition update <competition_id> <name> <description> <date>`
  - **Example**: `flask competition update 1 "New Name" "New Description" 2024-10-01`

### Result Commands
- **Command Group**: `result`
- **Description**: Commands related to result operations.

**Import Results from CSV**  
- **Command**: `result import`  
- **Description**: Imports competition results from a CSV file.  
- **Usage**: `flask result import <filename> <admin_id>`
- **Example**: `flask result import results.csv 2`

- **Add Result**: 
  - **Command**: `result add`
  - **Description**: Adds a result to a competition for a student.
  - **Usage**: `flask result add <competition_id> <user_id> <score> <rank> <time_taken> <problems_solved>`
  - **Example**: `flask result add 1 3 95 1 None 5`

- **List Results by Competition**: 
  - **Command**: `result list_by_competition`
  - **Description**: Lists all results for a competition.
  - **Usage**: `flask result list_by_competition <competition_id>`
  - **Example**: `flask result list_by_competition 1`

- **List Results by User**: 
  - **Command**: `result list_by_user`
  - **Description**: Lists all results for a user.
  - **Usage**: `flask result list_by_user <user_id>`
  - **Example**: `flask result list_by_user 3`

### Test Commands
- **Command Group**: `test`
- **Description**: Commands related to testing.

- **Run User Tests**: 
  - **Command**: `test user`
  - **Description**: Runs user tests.
  - **Usage**: `flask test user <type>`
  - **Example**: `flask test user unit`
