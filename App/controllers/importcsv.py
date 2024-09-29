import csv
from App.models import Competition, Result, User, Admin, Student
from App.database import db

def import_results_from_csv(csv_file):
    try:
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)

            users_to_create = {}  # Collect unique users and their types
            
            # First pass: gather unique users
            for row in reader:
                username = row['username']
                user_type = row['type']
                if username not in users_to_create:
                    users_to_create[username] = user_type
            
            file.seek(0)
            next(reader)

            # Second pass: process results and create users
            for row in reader:
                competition_id = int(row['competition_id'])
                username = row['username']
                score = float(row['score'])
                rank = int(row['rank'])
                problems_solved = int(row.get('problems_solved', 0))

                competition = Competition.query.get(competition_id)
                if not competition:
                    print(f"Competition ID {competition_id} does not exist. Skipping result for user {username}.")
                    continue

                user = User.query.filter_by(username=username).first()
                
                # Create a new user if not already present
                if not user:
                    user_type = users_to_create[username]
                    if user_type == 'admin':
                        user = Admin(username=username, password=username + "pass")
                    else:
                        user = Student(username=username, password=username + "pass")
                    
                    db.session.add(user)
                    db.session.commit()
                    print(f"User {username} created with ID: {user.id}")

                # Skip adding results for admins
                if user.type == 'admin':
                    print(f"Skipping result for admin {username} (ID: {user.id}).")
                    continue

                # Avoid duplicate results
                existing_result = Result.query.filter_by(competition_id=competition_id, user_id=user.id).first()
                if existing_result:
                    print(f"Duplicate result for user {username} (ID: {user.id}) in competition {competition_id}. Skipping.")
                    continue

                # Add result to the database
                result = Result(
                    competition_id=competition_id,
                    user_id=user.id,
                    score=score,
                    rank=rank,
                    problems_solved=problems_solved
                )

                db.session.add(result)
                db.session.commit()
                print(f"Added result for user {username} (ID: {user.id}) in competition {competition_id}.")

    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
    except KeyError as e:
        print(f"Error: Missing column - {e}")
    except ValueError as e:
        print(f"Error: Invalid value - {e}")
    except Exception as e:
        print(f"Error: {e}")
