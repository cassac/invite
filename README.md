# Invite App
Invitation and RSVP management application - Python/Flask App

Sends invitations via your Gmail account, tracks guests RSVP status
via link in email, upload photos for everyone to view before. Displays
event information and map for everyone to view. Users cannot view
pictures until they have uploaded one themselves.

Required Adjustments Before Use
- Edits need to be made to the email configurations in config.py
- Invitation.txt needs to be added to static/templates/email with customized message
  using 'guest' varibale passed through view. The body of the email can utilize
  dynamically generated URL's to allow for user's to RSVP by clicking on a link
  in the body of the email. Look at the view for guest_status() using this path 
  '/guest/<email>/<status>'. 
- Currently all passwords are set to the string in models.py User model. To assign
individual passwords and allow password hashing undo the commented-out lines
in the User model and adjust verify_password()
- Event details on dashboard.html

1) Install libraries via pip
```
pip install -r requirements.txt
```
2) Create database
```
python manage.py shell
```
```
db.create_all()
```

3) Create an admin
```
python manage.py shell
```
```
admin = User(name="Admin's Name", email="admin@example.com", is_admin=True)
```
```
db.session.add(admin)
```
```
db.session.commit()
```
4) Creating users (aka Guests)

```
python manage.py shell
```
```
guest = User(name="Guests's Name", email="guest@example.com", is_admin=False)
```
```
db.session.add(guest)
```
```
db.session.commit()
```
```
** To add multiple guests at once use: db.session.add_all([var1, var2, var3])

Passwords are automatically set to the string inside the models.py User model.

