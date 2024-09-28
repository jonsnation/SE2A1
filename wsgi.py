import click, pytest, sys, csv
from flask import Flask
from flask.cli import with_appcontext, AppGroup
from datetime import datetime

from App.database import db, get_migrate
from App.models import User, Competition, Result
from App.main import create_app
from App.controllers import (
    create_user, get_all_users_json, get_all_users,
    create_competition, get_all_competitions_json, get_all_competitions, get_competition_by_id, update_competition,
    add_result, get_results_by_competition, get_results_by_user,
    initialize, import_results_from_csv
)

app = create_app()
migrate = get_migrate(app)

# Initialize database command
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database initialized')

'''
User Commands
'''

user_cli = AppGroup('user', help='User object commands')

@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
@click.argument("role", default="student")  # Add role argument (default to 'student')
def create_user_command(username, password, role):
    user = create_user(username, password, role)  # Capture the returned user object
    print(f'User {username} created as {role} with ID: {user.id}!')  # Print the ID


@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    users = get_all_users() if format == 'string' else get_all_users_json()
    
    if format == 'string':
        # Print in tabular format
        print(f"{'ID':<10} {'Username':<20} {'Role':<10}")  # Header
        print("-" * 40)  # Separator
        for user in users:
            print(f"{user.id:<10} {user.username:<20} {user.type:<10}")  # Adjust field lengths as necessary
    else:
        # Print JSON format
        for user in users:
            print(user)  # Assuming user is a JSON object

        print(get_all_users_json())

app.cli.add_command(user_cli)

'''
Competition Commands
'''

competition_cli = AppGroup('competition', help='Competition object commands')

@competition_cli.command('create', help="Creates a new competition")
@click.argument('name')
@click.option('--description', default=None)
@click.option('--date', default=None)
@click.option('--admin-id', required=True, help='Admin ID creating the competition')
def create_competition_command(name, description, date, admin_id):
    # Convert date string to datetime object
    if date:
        date = datetime.strptime(date, '%Y-%m-%d')  # Adjust format if necessary
    competition = create_competition(name=name, description=description, date=date, admin_id=admin_id)
    
    if competition:
        print(f"Competition '{name}' created successfully with ID {competition.id}.")
    else:
        print(f"Failed to create competition '{name}'. Either the name is taken, or the admin ID is invalid.")


@competition_cli.command("list", help="Lists all competition names and IDs in a tabular format")
@click.argument("format", default="string")
def list_competitions_command(format):
    # Fetch competitions based on the specified format
    competitions = get_all_competitions_json() if format != 'string' else get_all_competitions()
    
    if competitions:
        # Print header
        print(f"{'ID':<5} {'Name':<30}")  # Adjust the width as necessary
        print("-" * 35)  # Print a separator line
        
        if format != 'string':
            # Assuming competitions is a list of dictionaries in JSON format
            for competition in competitions:
                print(f"{competition['id']:<5} {competition['name']:<30}")
        else:
            # Assuming competitions is a list of objects with 'id' and 'name' attributes
            for competition in competitions:
                print(f"{competition.id:<5} {competition.name:<30}")
    else:
        print("No competitions found.")


@competition_cli.command("update", help="Update competition details")
@click.argument("competition_id")
@click.argument("name", required=False)
@click.argument("description", required=False)
@click.argument("date", required=False)
def update_competition_command(competition_id, name, description, date):
    competition = update_competition(competition_id, name=name, description=description, date=date)
    if competition:
        print(f'Competition {competition_id} updated!')
    else:
        print(f'Competition {competition_id} not found!')

app.cli.add_command(competition_cli)

'''
Result Commands
'''

result_cli = AppGroup('result', help='Result object commands')

@result_cli.command("add", help="Add a result to a competition")
@click.argument("competition_id")
@click.argument("user_id")
@click.argument("score")
@click.argument("rank")
@click.argument("time_taken", default=None)
@click.argument("problems_solved", default=None)
def add_result_command(competition_id, user_id, score, rank, time_taken, problems_solved):
    # Fetch the user to check their role
    user = User.query.get(user_id)  # Adjust based on your actual user retrieval logic
    if user is None:
        print(f'Error: User with ID {user_id} does not exist.')
        return

    # Check if the user is an admin
    if user.type == 'admin':
        print(f'Error: Admin users cannot have results added.')
        return

    # Proceed to add the result if the user is not an admin
    result = add_result(
        competition_id=competition_id,
        user_id=user_id,
        score=score,
        rank=rank,
        time_taken=time_taken,
        problems_solved=problems_solved
    )
    print(f'Result for user {user_id} in competition {competition_id} added!')


@result_cli.command("list_by_competition", help="List all results for a competition")
@click.argument("competition_id")
def list_results_by_competition_command(competition_id):
    results = get_results_by_competition(competition_id)
    
    if results:
        # Print header
        print(f"{'ID':<5} {'Competition ID':<15} {'Competition Name':<25} {'User ID':<10} {'Username':<20} {'Score':<10} {'Rank':<5} {'Problems Solved':<15}")  
        print("-" * 110)  # Print a separator line
        
        for result in results:
            # Assuming result.get_json() returns a dictionary
            result_data = result.get_json()
            
            # Fetch the user by user_id
            user = User.query.get(result_data['user_id'])  # Adjust based on your actual user retrieval logic
            username = user.username if user else 'Unknown'  # Default to 'Unknown' if user not found
            
            print(f"{result_data['id']:<5} {result_data['competition_id']:<15} {result_data['competition_name']:<25} "
                  f"{result_data['user_id']:<10} {username:<20} {result_data['score']:<10} {result_data['rank']:<5} "
                  f"{result_data['problems_solved']:<15}")
    else:
        print(f'No results found for competition {competition_id}.')



@result_cli.command("list_by_user", help="List all results for a user")
@click.argument("user_id")
def list_results_by_user_command(user_id):
    results = get_results_by_user(user_id)
    
    if results:
        # Print header for tabular form
        print(f"{'Result ID':<10} {'Competition ID':<15} {'Competition Name':<25} {'User ID':<10} {'Score':<10} {'Rank':<5} {'Problems Solved':<15}")
        print("-" * 90)  # Print a separator line
        
        for result in results:
            result_json = result.get_json()  # Get the updated result JSON with names
            print(f"{result_json['id']:<10} {result_json['competition_id']:<15} {result_json['competition_name']:<25} "
                  f"{result_json['user_id']:<10} {result_json['score']:<10} {result_json['rank']:<5} {result_json['problems_solved']:<15}")
    else:
        print(f'No results found for user {user_id}.')


# Example for CSV error handling
@result_cli.command("import", help="Import results from a CSV file")
@click.argument("csv_file")  # This is your CSV file
@click.argument("admin_id", type=int)  # Admin ID as a positional argument
def import_results_from_csv_command(csv_file, admin_id):
    # Check if the admin exists
    admin = User.query.get(admin_id)
    if not admin or admin.type != 'admin':
        print(f"Error: User ID {admin_id} is not an admin.")
        return

    try:
        import_results_from_csv(csv_file)
        print(f"Results imported successfully from {csv_file}.")
    except FileNotFoundError:
        print(f"Error: The file {csv_file} was not found.")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {str(e)}")





app.cli.add_command(result_cli)

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(test)
