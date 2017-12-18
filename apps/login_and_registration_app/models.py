from __future__ import unicode_literals

from django.db import models

import re
import bcrypt
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r"^[a-zA-Z ,.'-]+$")

class UserValidator(models.Manager):
	def AddUser(self, name, alias, email, dob, password, confirm_password):
		errors = []
		# check if name is not blank and does not contain digits
		if len(name) < 3:
			errors.append("Name must be at least 3 charaters!")
		elif len(name) >= 3:	
			if any(char.isdigit() for char in name):
				errors.append("No numbers in the name field!")
			else:		 		
				if not NAME_REGEX.match(str(name)):
					errors.append("Please enter valid first and last name!")
				else:
					names = name.split(" ", 1)
					if len(names) < 2:
						errors.append("Please enter first AND last name!")		 	 
		if len(alias) < 3:
			errors.append("Alias must be at least 3 characters!")
		#check for valid DOB	
		if len(dob) < 1:
			errors.append("Date of Birth is required!")
		else:
			date = datetime.strptime(dob, '%Y-%m-%d')
			today = datetime.now()
			if date > today:
				errors.append("Date of Birth must be in the past!") 
		if len(password) < 8:
			errors.append("Password must be at least 8 characters long!")
		else:
			secure_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
		# check email an dmake sure it doesnt already exist!			
		if not EMAIL_REGEX.match(email):
			errors.append("Please enter a valid email address!")
		else:	
			emails = Users.objects.filter(email=email)
			if len(emails) != 0:	
				errors.append("Email already taken!")
		if password != confirm_password:
			errors.append("Passwords must match!")
		if len(errors) > 0:
			return errors	
		else:
			new_user = Users.objects.create(first_name=names[0], last_name=names[1], alias=alias, email=email, dob=dob, password=secure_password)
			return new_user	
	def login(self, email, password):
		users = Users.objects.filter(email=email)
		if len(users) == 0:
			return "Invalid email!"
		elif bcrypt.checkpw(password.encode(), users[0].password.encode()) == False:
			return "Incorrect password!"
		else:	
			return users[0]	

class Users(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	dob = models.DateField()
	friends = models.ManyToManyField("self")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserValidator()
	def __repr__(self):
		return "<Users object: {} {} {}>".format(self.first_name, self.last_name, self.alias, self.email)

