from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
from django.contrib.auth.models import User as auth
from django.contrib.auth import authenticate, logout
from django.db.models import Q
import datetime
from django.core.mail import send_mail



user_role = ''

# home page.
def home(request):
    data = models.Mentor.objects.filter(status = 'accepted')[:3]
    if user_role == '':
        return render(request, 'home.html', {'data': data})
    elif user_role == 'user':
        return redirect('view_mentors')
    elif user_role == 'mentor':
        return redirect('patient_request')
    else:
        return redirect('view_mentors_request')


def login(request):
    global user_role, user
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if email == 'admin':
            try:
                user = authenticate(username='admin', password=password)
                if user is not None:
                    user_role = 'admin'
                    return redirect('view_mentors_request')
                else:
                    return HttpResponse('<script>alert("Incorrect Password"); window.open("login","_self")</script>')
            except:
                return HttpResponse('<script>alert("Incorrect Password"); window.open("login","_self")</script>') 
        else:
            user = authenticate(request, username=email, password=password)
            if user is not None:
                request.session['user'] = email
                try:
                    is_user = models.User.objects.get(email=email)
                    request.session['id'] = is_user.user_id
                    user_role = 'user'
                    return redirect('view_mentors')
                except:
                    try:
                        is_mentor = models.Mentor.objects.get(email=email)
                        request.session['id'] = is_mentor.mentor_id
                        if is_mentor.status == 'requested':
                            return HttpResponse('<script>alert("Your Request has been sent. Once the admin approve you can login to your account"); window.open("home","_self")</script>')
                        else:
                            user_role = 'mentor'
                            return redirect('patient_request')
                    except:
                        user_role = 'admin'
                        return redirect('view_mentors_request')
            else:
                return HttpResponse('<script>alert("Incorrect Password"); window.open("login","_self")</script>') 
    else:
        return render(request, 'login.html')
    


def signup(request):
    global user_role
    if(request.method == 'POST'):
      user_db = models.User()
      mentor_db = models.Mentor()
      role = request.POST['role']
      if role == 'mentor':
          mentor_db.name = request.POST['name']
          mentor_db.phone = request.POST['phone']
          mentor_db.email = request.POST['email']
          password = request.POST['password']
          mentor_db.role = role
          mentor_db.status = 'requested'
          mentor_db.profilepic = request.FILES['profile_image']
          mentor_db.fb = request.POST['fbid']
          mentor_db.instagram = request.POST['Instaid']
          mentor_db.save()
          id = models.Mentor.objects.get(email=mentor_db.email)
          msg = f'Hi {mentor_db.name},\nYour request for creating account has been received. Once the admin has reviewed the request and approved, you will be notified and can login to your account.\n\n\nRegards,\nWhealth Management'
          try:
              auth.objects.create_user(username=mentor_db.email, password=password)
              send_mail('Account Registration', msg, 'whealthmentorapp@whealthmentor.com', [mentor_db.email], fail_silently=False)
          except:
            return HttpResponse('<script>alert("Email Id already used"); window.open("login","_self")</script>')
          return HttpResponse('<script>alert("Your Request has been sent. Once the admin approve you can login to your account"); window.open("home","_self")</script>')
        #   return redirect('patient_request')
      else:
          user_db.name = request.POST['name']
          user_db.phone = request.POST['phone']
          user_db.email = request.POST['email']
          password = request.POST['password']
          user_db.role = role
          user_db.save()
          id = models.User.objects.get(email=user_db.email)
          request.session['id'] = id.user_id 
          request.session['user'] = user_db.email
          try:
              auth.objects.create_user(username=user_db.email, password=password)
          except:
                return HttpResponse('<script>alert("Email Id already used"); window.open("signup","_self")</script>')
          authenticate(username=user_db.email, password=password)
          user_role = 'user'
          return redirect('view_mentors')
    else:
        return render(request, 'signup.html')


def user_logout(request):
    try:
        del request.session['user']
        del request.session['id']
    except:
        pass
    global user_role
    user_role = ''
    logout(request)
    return redirect('home')


def viewMentors(request):
    data = models.Mentor.objects.filter(status = 'accepted')
    return render(request, 'mentors.html', {'data': data})

# home ends

# admin page

def view_mentors_request(request):
    is_admin = admin_check()
    if is_admin == True:
        data = models.Mentor.objects.filter(status = 'requested')
        return render(request, 'admin/mentor_request.html', {'data': data})
    else:
        return is_admin


def accept_mentor(request, id):
    is_admin = admin_check()
    if is_admin == True:
        db = models.Mentor.objects.get(mentor_id = id)
        db.status = 'accepted'
        db.save()
        msg = f'Hi {db.name},\nYour request has reviewed and approved, you will be now able to login into your account.\n\n\nRegards,\nWhealth Management'
        send_mail('Account Registration', msg, 'whealthmentorapp@whealthmentor.com', [db.email], fail_silently=False)
        return redirect('view_mentors_request')
    else:
        return is_admin


def reject_mentor(request, id):
    is_admin = admin_check()
    if is_admin == True:
        db = models.Mentor.objects.get(mentor_id = id)
        db.status = 'rejected'
        db.save()
        msg = f'Hi {db.name},\nYour request has reviewed and unfortunately we were sorry to inform that the request has been rejected. If you think it was a mistake feel free to mail our supporting team.\nwhealthmentorapp@gmail.com\n\n\nRegards,\nWhealth Management'
        send_mail('Account Registration', msg, 'whealthmentorapp@whealthmentor.com', [db.email], fail_silently=False)
        return redirect('view_mentors_request')
    else:
        return is_admin


def admin_view_mentors(request):
    is_admin = admin_check()
    if is_admin == True:
        data = models.Mentor.objects.filter(status = 'accepted')
        return render(request, 'admin/adminViewMentors.html', {'data': data})
    else:
        return is_admin


def view_regected_mentors(request):
    is_admin = admin_check()
    if is_admin == True:
        data = models.Mentor.objects.filter(status = 'rejected')
        return render(request, 'admin/mentor_regected.html', {'data': data})
    else:
        return is_admin


def admin_view_patients(request):
    is_admin = admin_check()
    if is_admin == True:
        data = models.User.objects.all()
        return render(request, 'admin/adminViewpatients.html', {'data': data})
    else:
        return is_admin


def admin_view_messages(request):
    is_admin = admin_check()
    if is_admin == True:
        mentor = models.report.objects.filter(role = 'mentor')
        user = models.report.objects.filter(role = 'user')
        return render(request, 'admin/adminViewMessages.html', {'user': user, 'mentor': mentor})
    else:
        return is_admin


def admin_reply_message(request, id):
    is_admin = admin_check()
    if is_admin == True:
        data = models.report.objects.get(id=id)
        if request.method == 'POST':
            data.reply = request.POST['reply']
            data.save()
            return redirect('admin_view_messages')
        return render(request, 'admin/reply.html', {'data': data})
    else:
        return is_admin


def admin_profile(request):
    is_admin = admin_check()
    if is_admin == True:
        if request.method == 'POST':
            user = authenticate(username = 'admin', password = request.POST['current_password'])
            print(request.POST['current_password'], user)
            if user is not None:
                user.set_password(request.POST['new_password'])
                user.save()
                print('SAS')
        return render(request, 'admin/profile.html')
    else:
        return is_admin

# admin ends

    
# mentor page

def patients_request(request):
    is_mentor = mentor_check()
    if is_mentor == True:
        patient_requests = models.PatientRequests.objects.filter(mentor_id = request.session['id'], status = 'requested')
        return render(request, 'mentor/patient_request.html', {'data': patient_requests})
    else:
        return is_mentor


def accept_patient_request(request, id):
    is_mentor = mentor_check()
    if is_mentor == True:
        db = models.PatientRequests.objects.get(user_id = id, mentor_id = request.session['id'])
        db.status = 'accepted'
        db.save()
        return redirect('accepted_patients')
    else:
        return is_mentor
    

def reject_patient_request(request):
    is_mentor = mentor_check()
    if is_mentor == True:
        db = models.PatientRequests.objects.get(user_id = id)
        db.status = 'rejected'
        db.save()
        return redirect('patient_request')
    else:
        return is_mentor


def accepted_patients(request):
    is_mentor = mentor_check()
    if is_mentor == True:
        data = models.PatientRequests.objects.filter(status = 'accepted', mentor_id = request.session['id'])
        return render(request, 'mentor/accepted_patients.html', {'data': data})
    else:
        return is_mentor


def mentor_profile(request):    
    is_mentor = mentor_check()
    if is_mentor == True:
        email = request.session['user']
        db = models.Mentor.objects.get(email=email)
        if request.method == 'POST':
            db.name  = request.POST['name']
            db.phone = request.POST['phone']
            db.fb = request.POST['fb']
            db.instagram = request.POST['instagram']
            if (request.POST['password'] != ''):
                old_password = request.POST['old-password']
                if authenticate(username = request.session['user'], password=old_password):
                    user = auth.objects.get(username = request.session['user'])
                    user.set_password(request.POST['password'])
                    user.save()
                else:
                    return HttpResponse('<script>alert("Incorrect Password"); window.open("mentor_profile","_self")</script>')
            db.save()
        return render(request, 'mentor/profile.html', {'data' : db})
    else:
        return is_mentor


def mentor_chat(request):
    is_mentor = mentor_check()
    if is_mentor == True:
        if request.method == 'POST':
            userid = request.POST['userid']
            db = models.chat.objects.get(user_id=userid)
            db.reply = request.POST['reply']
            db.save()
        data = models.chat.objects.filter(mentor_id=request.session['id'])
        print(data)
        return render(request, 'mentor/chat.html', {'data': data})
    else:
        return is_mentor


def mentor_reply_chat(request, id):
    is_mentor = mentor_check()
    if is_mentor == True:
        db = models.chat.objects.get(id=id)
        if request.method == 'POST':
            db.reply = request.POST['reply']
            db.save()
            return redirect('mentor_chat')
        else:
            return render(request, 'mentor/reply.html', {'data': db})
    else:
        return is_mentor


def view_diary_writings(request):
    is_mentor = mentor_check()
    if is_mentor == True:
        data = models.Diary_writings.objects.filter(mentor_id = request.session['id'])
        return render(request, 'mentor/view_diary_writings.html', {'data': data})
    else:
        return is_mentor


def reply_to_diary_writings(request, id):
    is_mentor = mentor_check()
    if is_mentor == True:
        db = models.Diary_writings.objects.get(id = id)
        if request.method == 'POST':
            db.reply = request.POST['reply_msg']
            db.save()
            return redirect('view_diary_writings')
        return render(request, 'mentor/dairy_reply.html', {'data' : db})
    else:
        return is_mentor


def send_motivations(request):
    is_mentor = mentor_check()
    if is_mentor == True:
        db = models.motivations()
        if request.method == 'POST':
            db.motivation = request.POST['motivational-content']
            db.Mentor = models.Mentor.objects.get(mentor_id = request.session['id'])
            db.save()
        data = models.motivations.objects.filter(Mentor_id = request.session['id'])
        return render(request, 'mentor/send_motivations.html', {'data': data})
    else:
        return is_mentor


def sent_complaints(request):
    is_mentor = mentor_check()
    if is_mentor == True:
        db = models.report()
        if request.method == 'POST':
            db.report_msg = request.POST['reportmsg']
            db.mentor = models.Mentor.objects.get(mentor_id = request.session['id'])
            db.role = user_role
            db.save()
        data = models.report.objects.filter(mentor_id = request.session['id'], role = user_role)
        print(request.session['id'], user_role)
        for i in data:
            print(i)
        return render(request, 'mentor/sent_complaints.html', {'data': data})
    else:
        return is_mentor

# mentor ends

# user starts

def user_profile(request):
    is_user = user_check()
    if is_user == True:
        email = request.session['user']
        db = models.User.objects.get(email=email)
        if request.method == 'POST':
            db.name = request.POST['name']
            db.phone = request.POST['phone']
            if request.POST['password'] != '':
                user = authenticate(username = request.session['user'], password = request.POST['old_password'])
                if user is not None:
                    user.set_password(request.POST['password'])
                    user.save()
                else:
                    return HttpResponse('<script>alert("Incorrect Password"); window.open("user_profile","_self")</script>')
            db.save()
        return render(request, 'client/profile.html', {'data' : db})
    else:
        return is_user


def user_view_mentors(request):
    is_user = user_check()
    if is_user == True:
        data = models.Mentor.objects.all()
        return render(request, 'client/mentors.html', {"data":data})
    else:
        return is_user


def requst_mentor(request):
    is_user = user_check()
    if is_user == True:
        if request.method == 'POST':
            id = request.POST['mentorid']
            db = models.PatientRequests()
            if models.PatientRequests.objects.filter(user_id = request.session['id'], mentor_id = id).exists():
                return HttpResponse('<script>alert("Sorry, Already Requested to this mentor"); window.open("view_mentors","_self")</script>')
            else:
                user = models.User.objects.get(email = (request.session['user']))
                mentor = models.Mentor.objects.get(mentor_id=id)
                db.user = user
                db.mentor = mentor
                db.status = 'requested'
                db.msg = request.POST['msg']
                db.save()
            return redirect('view_requested_mentors')
        else:
            return redirect('view_requested_mentors')

    else:
        return is_user


def view_requested_mentors(request):
    is_user = user_check()
    if is_user:
        data = models.PatientRequests.objects.filter(status = 'requested', user_id = request.session['id'])
        return render(request, 'client/requested_mentors.html', {'data': data})
    else:
        return is_user

def view_accepted_mentors(request):
    is_user = user_check()
    if is_user:
        data = models.PatientRequests.objects.filter(status = 'accepted', user_id = request.session['id'])
        return render(request, 'client/accepted_mentors.html', {'data': data})
    else:
        return is_user


def chat(request):
    is_user = user_check()
    if is_user:
        db = models.chat()
        if request.method == 'POST':
            db.chat = request.POST['chat']
            mentor = request.POST['mentor']
            db.user = models.User.objects.get(user_id=request.session['id'])
            db.mentor = models.Mentor.objects.get(mentor_id=mentor)
            db.save()
        mentors = models.PatientRequests.objects.filter(user_id=request.session['id'], status='accepted')
        data = models.chat.objects.filter(user_id=request.session['id'])
        return render(request, 'client/chat.html', {'data': data, 'mentors': mentors})
    else:
        return is_user


def write_diary(request):
    is_user = user_check()
    if is_user:
        db = models.Diary_writings()
        date = datetime.date.today().strftime(f"%d/%m/%Y")
        if request.method == 'POST':
            db.dairy = request.POST['dairy'][10:]
            db.user = models.User.objects.get(user_id=request.session['id'])
            db.mentor = models.Mentor.objects.get(mentor_id=request.POST['mentorid'])
            db.date = date
            db.save()

        data = models.Diary_writings.objects.filter(user_id=request.session['id'])
        mentors = models.PatientRequests.objects.filter(user_id=request.session['id'], status='accepted')
        return render(request, 'client/write_diary.html', {'dairy': data, 'mentors':mentors, 'date': date})
    else:
        return is_user


def view_motivations(request):
    is_user = user_check()
    if is_user:
        mentor_id = []
        mentors = models.PatientRequests.objects.filter(user_id = request.session['id'], status = 'accepted')
        for i in mentors:
            mentor_id.append(i.mentor_id)
            print(mentor_id)
        data = models.motivations.objects.filter(Q(Mentor_id__in=mentor_id))
        return render(request, 'client/view-motivations.html', {'data': data})
    else:
        return is_user
    

def report(request):
    is_user = user_check()
    if is_user:
        db = models.report()
        if request.method == 'POST':
            db.report_msg = request.POST['reportmsg']
            db.user = models.User.objects.get(user_id = request.session['id'])
            db.role = user_role
            db.save()
        
        data = models.report.objects.filter(user_id = request.session['id'], role = user_role)
        return render(request, 'client/report.html', {'data': data})
    else:
        return is_user

# user ends


# common function

def mentor_check():
    if user_role == 'mentor':
        return True
    else:
        return HttpResponse('<script>alert("Sorry You are not autherized to go to this page"); window.open("home","_self")</script>')
    

def user_check():
    if user_role == 'user':
        return True
    else:
        return HttpResponse('<script>alert("Sorry You are not autherized to go to this page"); window.open("home","_self")</script>')
         
    

def admin_check():
    if user_role == 'admin':
        return True
    else:
        return HttpResponse('<script>alert("Sorry You are not autherized to go to this page"); window.open("home","_self")</script>')