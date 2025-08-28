"""
Implement User Management System
def x
class x; enum o
절차지향
1. 로그인
2.
viewer : 자신의 정보만 수정가능 , 자신의 계정만 삭제가능
editor : 모든 사용자 정보 수정가능, 자신의 계정만 삭제가능
admin : 모든 사용자 정보 수정가능, 모든 계정 삭제 가능
"""
from enum import Enum
import json

class ActionFlow(Enum):
     LOGIN = "login"
     SELECT_MENU = "select_menu"
     EDIT = "edit"
     DELETE = "delete"
     EXIT = "exit"

class Role(Enum):
     ADMIN = "admin"
     EDITOR = "editor"
     VIEWER = "viewer"

class RolePermission(Enum):
     EDIT_ALL = "edit_all"
     EDIT_ONLY = "edit_only"
     DELETE_ALL = "delete_all"
     DELETE_ONLY = "delete_only"


user_permissions_dict = {
     Role.ADMIN: {RolePermission.EDIT_ALL, RolePermission.DELETE_ALL},
     Role.EDITOR: {RolePermission.EDIT_ALL, RolePermission.DELETE_ONLY},
     Role.VIEWER: {RolePermission.EDIT_ONLY, RolePermission.DELETE_ONLY}
}

user_db = {
     "admin": {"passwd": "0000", "role": "admin"},
     "editor": {"passwd": "0000", "role": "editor"},
     "mark": {"passwd": "0000", "role": "viewer"},
     "james": {"passwd": "0000", "role": "viewer"},
     "tom": {"passwd": "0000", "role": "viewer"}
}


action_flow = ActionFlow.LOGIN
print("login")
username = None
passwd = None
user = None
while action_flow == ActionFlow.LOGIN:
     username = input("username: ")
     passwd = input("password: ")

     user = user_db.get(username)

     if user and user["passwd"] == passwd:
          print(f"welcome, {username}!")
          action_flow = ActionFlow.SELECT_MENU
     else:
          print("invalid username or password.")

while action_flow == ActionFlow.SELECT_MENU:
     print("""
1. edit
2. delete
3. exit """.strip())
     selection = input("select an number:")

     user_role = Role(user["role"])
     permissions = user_permissions_dict[user_role]

     if selection == "1":
          if RolePermission.EDIT_ALL in permissions or RolePermission.EDIT_ONLY in permissions:
               action_flow = ActionFlow.EDIT
          else:
               print("no permission to edit~")
     elif selection == "2":
          if RolePermission.DELETE_ALL in permissions or RolePermission.DELETE_ONLY in permissions:
               action_flow = ActionFlow.DELETE
          else:
               print("no permission to delete~")
     elif selection == "3":
          action_flow = ActionFlow.EXIT
     else:
          print("wrong input, try again")

     while action_flow == ActionFlow.EDIT:
          edit_username = None
          if RolePermission.EDIT_ONLY in permissions:
               edit_username = username
          else:
               edit_username = input("put username to edit:")

          if edit_username == username or user_role == Role.ADMIN or user_role == Role.EDITOR:
               if edit_username in user_db:
                    new_passwd = input(f"put new password({edit_username}): ")
                    user_db[edit_username]["passwd"] = new_passwd
                    print(f"{edit_username} < changed")
                    print(json.dumps(user_db, indent=4))
               else:
                    print(f"{edit_username} < not exists")
          else:
               print(
                   f"no permission to edit or {edit_username} is not your account")
          action_flow = ActionFlow.SELECT_MENU

     while action_flow == ActionFlow.DELETE:
          del_username = None
          if RolePermission.DELETE_ONLY in permissions:
               del_username = username
          else:
               del_username = input("put username to delete:")

          if del_username == username or user_role == Role.ADMIN:
               if del_username in user_db:
                    user_db.pop(del_username)
                    print(f"{del_username} < deleted")
                    print(json.dumps(user_db, indent=4))
               else:
                    print(f"{del_username} < not exists")
          else:
               print(f"no permission to delete or {del_username} is not your account")
          action_flow = ActionFlow.SELECT_MENU

print("bye~")

     



