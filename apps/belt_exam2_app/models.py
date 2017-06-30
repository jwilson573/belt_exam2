from __future__ import unicode_literals
import bcrypt
from django.db import models

class UserManager(models.Manager):
    
    def validate(self, form):
        
        errors = []
        user_record = User.objects.filter(alias=form['alias']).first()
        email_record = User.objects.filter(email=form['email']).first()
        
        if user_record:
            errors.append("Alias already exists.")
        
        if email_record:
            errors.append("Email already exists")

        if len(form['name']) < 3 or len(form['alias']) < 3:
            errors.append("Name fields must be at least 3 characters.")
            
        
        if len(form['password']) < 8:
            errors.append("Password must be at least 8 characters.")

        if len(form['email']) <= 7:
            errors.append("Please enter a valid email address.")
        
        if form['password'] != form['pwconfirm']:
            errors.append("Passwords do not match.")
            

        if form['DOB'] == '':
            errors.append("Please enter your date of birth.")
        
        return errors
    
    
    def register(self, form):

        errors = []
        
        password = str(form['password'])
        encryptedpw = bcrypt.hashpw(password, bcrypt.gensalt())
        
        user = User.objects.create(
                name = form['name'],
                alias = form['alias'],
                email = form['email'],
                DOB = str(form['DOB']),
                password = encryptedpw,

            )
        return user

    
    def validate_login(self, form):
        print "Inside the login_validate method"

        
        errors = []
        user_check = User.objects.filter(alias=form['userlogin']).first()
        # print user_check

        if user_check == None:
            errors.append("User not in database")
            return errors
    
        if user_check:
            password = str(form['passlogin'])
            user_pass = str(user_check.password)

            encryptedpw = bcrypt.hashpw(password, user_pass)

            if encryptedpw == user_pass:
                return user_check
            
            errors.append("Invalid Password")
        
        return errors

class User(models.Model):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    DOB = models.DateField(auto_now=False, blank=True, null=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s' %(self.name, self.alias)

    objects = UserManager()



class Poke(models.Model):
    poker = models.ForeignKey(User, related_name="poked")
    pokee = models.ForeignKey(User, related_name="poked_by")
     

    def __str__(self):
        return '%s %s' %(self.poker.name, self.pokee.name)

    