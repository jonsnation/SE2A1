import csv
from App.models import Competition, Result, User, Admin, Student
from App.database import db

def import_results_from_csv(csv_file):
    try:
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            users_to_create = {}  # Dictionary to hold unique users to create
            
            # First pass: collect users and their types
            for row in reader:
                username = row['username']
                user_type = row['type']  # Read user type

                # Store unique users with their type in a dictionary
                if username not in users_to_create:
                    users_to_create[username] = user_type
            
            # Reset file pointer to read results again
            file.seek(0)
            next(reader)  # Skip header again after resetting

            # Second pass: process results and create users
            for row in reader:
                competition_id = int(row['competition_id'])  # Convert to integer
                username = row['username']  # Read username
                score = float(row['score'])  # Convert to float
                rank = int(row['rank'])  # Convert to integer
                problems_solved = int(row.get('problems_solved', 0))  # Default to 0 if not present

                # Check if the competition exists
                competition = Competition.query.get(competition_id)
                if not competition:
                    print(f"Competition ID {competition_id} does not exist. Skipping result for user {username}.")
                    continue

                # Check if the user already exists
                user = User.query.filter_by(username=username).first()
                
                # If user does not exist, create a new one
                if not user:
                    user_type = users_to_create[username]  # Get the user type from the dictionary
                    if user_type == 'admin':
                        user = Admin(username=username, password=username + "pass")  # Create Admin instance
                    else:
                        user = Student(username=username, password=username + "pass")  # Create Student instance
                    
                    db.session.add(user)
                    db.session.commit()  # Commit to get the user_id if it is auto-incremented
                    print(f"User {username} created with ID: {user.id}")

                # Prevent adding results for admins
                if user.type == 'admin':
                    print(f"Skipping result for admin {username} (ID: {user.id}). Admins can't have results.")
                    continue

                # Check if the result already exists to prevent duplication
                existing_result = Result.query.filter_by(competition_id=competition_id, user_id=user.id).first()
                if existing_result:
                    print(f"Duplicate result found for user {username} (ID: {user.id}) in competition {competition_id}. Skipping.")
                    continue

                # Add result to the database
                result = Result(
                    competition_id=competition_id,
                    user_id=user.id,  # Use the newly created or found user ID
                    score=score,
                    rank=rank,
                    problems_solved=problems_solved
                )

                db.session.add(result)  # Add the result to the session
                db.session.commit()  # Commit the transaction
                print(f"Added result for user {username} (ID: {user.id}) in competition {competition_id}.")

    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
    except KeyError as e:
        print(f"Error: Missing expected column in CSV file - {e}")
    except ValueError as e:
        print(f"Error: Invalid value - {e}")
    except Exception as e:
        print(f"Error: {e}")
