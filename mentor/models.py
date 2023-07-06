from django.db import models

# Create your models here.
    
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    phone = models.CharField(max_length=25)
    email = models.EmailField(max_length=25)
    role = models.CharField(max_length=20)

    class Meta:
        db_table = 'User'


class Mentor(models.Model):
    mentor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    phone = models.CharField(max_length=25)
    email = models.EmailField(max_length=25)
    role = models.CharField(max_length=25)
    status = models.CharField(max_length=20)
    fb = models.CharField(max_length=50)
    instagram = models.CharField(max_length=50)
    profilepic = models.FileField(upload_to='mentorImage')

    class Meta:
        db_table = 'Mentor Table'


class AdminUser(models.Model):
    name = models.CharField(max_length=25)
    email = models.EmailField(max_length=25)
    phone = models.CharField(max_length=25)

    class Meta:
        db_table = 'AdminUser'


class PatientRequests(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    msg = models.CharField(max_length=250)
    class Meta:
        db_table = 'PatientRequests'


class Diary_writings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    dairy = models.CharField(max_length=500)
    reply = models.CharField(max_length=250)
    date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'Dairy_writings'


class chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    chat = models.CharField(max_length=200)
    reply = models.CharField(max_length=200)

    class Meta:
        db_table = 'Chat'


class report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, default=None)
    report_msg = models.CharField(max_length=250)
    role = models.CharField(max_length=50)
    reply = models.CharField(max_length=250)

    class Meta:
        db_table = 'Reports'


class motivations(models.Model):
    Mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    motivation = models.CharField(max_length=250)

    class Meta:
        db_table = 'motivation'

