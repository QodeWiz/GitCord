from src.database.models import Database

# test database
db = Database()

# test linking a user
db.link_user("123456789", "ishqa")
print("user linked successfully")

# test getting the user
github_username = db.get_linked_github("123456789")
print(f"linked github username: {github_username}")

# test saving a repo
db.save_repo("123456789", "microsoft", "vscode", "secret123", "987654321")
print("repo saved")

# test getting a repo 
repo = db.get_repo_by_owner_name("microsoft", "vscode")
print(f" found repo: {repo}")