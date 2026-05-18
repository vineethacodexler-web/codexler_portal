from django.shortcuts import render, redirect
from . models import *
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, auth
from . decorators import *
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from datetime import date
from django.core import serializers
import json
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.utils import timezone
from django.core.files.storage import FileSystemStorage, default_storage
import json
from django.shortcuts import render
@login_required
@logged_inn2


def admin_home(request):
    # Get the current logged-in user based on the session
    bok = Registration.objects.get(id=request.session['logg'])
    create_pro = CreateProject.objects.all()
    # Get all employees
    gtt = Registration.objects.filter(User_role='employee')
    total_project = CreateProject.objects.count()
    total_timesheet = Create_Timesheet_Line.objects.count()
    total_staffs = Registration.objects.exclude(User_role='admin').count()
    user = request.user
    leave_balance, _ = LeaveBalance.objects.get_or_create(staff=user)
    total_projects = CreateProject.objects.all()

    # Get the first employee (can be replaced with specific logic)
    df = Registration.objects.filter(User_role='employee').first()

    # Get all Registration records (this is the complete list of employees)
    k = Registration.objects.all()

    # Get the attendance records for the current logged-in user
    attendance_records = Attendance.objects.filter(employee=bok)

    leave_total = LeaveApplication.objects.count()
    leaves = LeaveApplication.objects.select_related('staff').all()

    # If you need to display total working days and total working hours, you can aggregate that
    total_working_days = attendance_records.count()
    total_working_minutes = sum(
        (att.check_out_time - att.check_in_time).total_seconds() / 60
        for att in Attendance.objects.filter(employee=bok)
        if att.check_in_time and att.check_out_time  # Ensure both times exist
    )

    context = {
        'k': k,
        'df': df,
        'gtt': gtt,
        'bok': bok,
        'attendance_records': attendance_records,
        'total_working_days': total_working_days,
        'total_working_minutes':  round(total_working_minutes, 2),
        'leave_total':leave_total,
        'leaves':leaves,
        'create_pro':create_pro,
        'total_project':total_project,
        'total_timesheet':total_timesheet,
        'total_staffs':total_staffs,
        'leave_balance':leave_balance,
        'total_projects':total_projects,
    }

    return render(request, 'admin_home.html', context)


def all_view_timesheet(request):

    bok = Registration.objects.get(id=request.session['logg'])

    # Fetch timesheets related to the logged-in staff
    timesheets = Create_Timesheet_Line.objects.filter(staff_list_id=bok.id)



    # Define `timesheet` before using it
    if timesheets.exists():  # Ensure there's at least one timesheet
        timesheet = timesheets.first()  # Get the first timesheet line
        t = Create_Timesheet.objects.filter(id=timesheet.timesheet_id)
    else:
        t = Create_Timesheet.objects.none()  # Return an empty queryset if no timesheets exist

    return render(request, 'all_view_timesheet.html', {
        't': t,
        'bok': bok,
        'timesheets':timesheets
    })



def all_view_timesheet_admin(request):
    bok = get_object_or_404(Registration, id=request.session.get('logg'))
    view_s =  Registration.objects.filter(User_role = 'employee')
    all_timesheet = Create_Timesheet_Line.objects.all()


    # Define `timesheet` before using it
    if all_timesheet.exists():  # Ensure there's at least one timesheet
        timesheet = all_timesheet.first()  # Get the first timesheet line
        t = Create_Timesheet.objects.filter(id=timesheet.timesheet_id)
    else:
        t = Create_Timesheet.objects.none()  # Return an empty queryset if no timesheets exist

    return render(request, 'all_view_timesheet_admin.html', {
        't': t,
        'bok': bok,
        'all_timesheet': all_timesheet,
        'view_s':view_s
    })


def all_view_timesheet_admins(request):
    bok = get_object_or_404(Registration, id=request.session.get('logg'))
    view_s =  Registration.objects.filter(User_role = 'employee')
    all_timesheet = Create_Timesheet_Line.objects.all()


    # Define `timesheet` before using it
    if all_timesheet.exists():  # Ensure there's at least one timesheet
        timesheet = all_timesheet.first()  # Get the first timesheet line
        t = Create_Timesheet.objects.filter(id=timesheet.timesheet_id)
    else:
        t = Create_Timesheet.objects.none()  # Return an empty queryset if no timesheets exist

    return render(request, 'all_view_timesheet_admins.html', {
        't': t,
        'bok': bok,
        'all_timesheet': all_timesheet,
        'view_s':view_s
    })


def logged_out(request):
    del request.session['logg']
    auth.logout(request)
    if 'logg' in request.session:
        del request.session['logg']
        return redirect('login')
    return redirect('login')


from django.core.exceptions import MultipleObjectsReturned

def login(request):
    if request.method == 'POST':
        username = request.POST.get("user_name")
        password = request.POST.get("pword")
        user = auth.authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Username or Password is Incorrect')
            return render(request, 'login.html')
        auth.login(request, user)

        try:
            registration = Registration.objects.get(user=user, Password=password)
            usertype = registration.User_role
            if usertype == 'admin':
                request.session['logg'] = registration.id
                return redirect("admin_home")
            elif usertype == 'employee':
                request.session['logg'] = registration.id
                registration.save()
                return redirect('employee_home')
            elif usertype == 'accounts':
                request.session['logg'] = registration.id
                registration.save()
                return redirect('f_dashboard')
            else:
                messages.error(request, 'Your access to the website is blocked. Please contact admin')
                return render(request, 'login.html')
        except Registration.DoesNotExist:
            messages.error(request, 'Username or password entered is incorrect')
            return render(request, 'login.html')
        except MultipleObjectsReturned:

            registrations = Registration.objects.filter(user=user, Password=password)
            return render(request, 'choose_account.html', {'registrations': registrations})
    else:
        return render(request, 'login.html')




def delete_admin(request, id):
    bb1 = Registration.objects.get(id = id)
    User.objects.get(email = bb1.Email).delete()
    messages.success(request, 'You have successfully resigned from administration')
    return redirect('home')

def edit_admin(request):
    bok = Registration.objects.get(id=request.session['logg'])
    gtt = Registration.objects.filter(User_role = 'admin')
    bb1 = Registration.objects.get(User_role = 'admin')
    um = User.objects.get(email=bb1.Email)
    return render(request, 'update_adminn.html',{'bb1':bb1,'um':um,'gtt':gtt,'bok':bok})

from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Registration

def bnb(request):
    bb1 = Registration.objects.get(User_role='admin')
    um = bb1.user

    if request.method == 'POST':
        first = request.POST.get('first')
        designatio = request.POST.get('designatio')
        em = request.POST.get('em')
        loc = request.POST.get('loc')
        mobile = request.POST.get('mobile')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        user_name = request.POST.get('user_name')
        psw = request.POST.get('psw')

        # Image upload
        if 'photo' in request.FILES:
            bb1.Image = request.FILES['photo']

        # Check username uniqueness
        if User.objects.exclude(id=um.id).filter(username=user_name).exists():
            messages.error(request, 'Username already taken')
            return render(request, 'admin_home.html', {'bb1': bb1, 'um': um})

        # Update User model
        um.username = user_name
        um.email = em
        if psw:
            um.password = make_password(psw)
        um.save()

        # Update Registration model
        bb1.First_name = first
        bb1.Designation = designatio
        bb1.Email = em
        bb1.Location = loc
        bb1.Mobile_Number = mobile
        bb1.Gender = gender
        bb1.Address = address
        if psw:
            bb1.Password = psw

        bb1.user = um
        bb1.save()

        messages.success(request, 'Profile Updated Successfully')
        return redirect('admin_home')

    return render(request, 'admin_home.html', {'bb1': bb1, 'um': um})

def del_admin(request, id):
    bb1 = Registration.objects.get(id = id)
    User.objects.get(email = bb1.Email).delete()
    messages.success(request, 'You have successfully resigned from administration')
    return redirect('home')

def admin_rg(request):
    if request.method == 'POST':
        lk = Registration.objects.all()
        for t in lk:
            if t.User_role == 'admin':
                messages.success(request, 'You are not allowed to be registered as admin')
                return redirect('home')
        x = datetime.now()
        z = x.strftime("%Y-%m-%d")
        admin_id = request.POST.get('admin_id')
        first_name = request.POST.get('first_name')
        designation = request.POST.get('designation')
        location = request.POST.get('location')

        mobile_number = request.POST.get('mobile_number')
        email = request.POST.get('email')
        psw = request.POST.get('psw')
        gender = request.POST.get('gender')
        useragreement = request.POST.get('useragreement')
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        fs.save(photo.name, photo)
        admin = request.POST.get('adminn1')
        reg1 = Registration.objects.all()
        for i in reg1:
            if i.Email == email:
                messages.success(request, 'User already exists')
                return render(request, 'register_admin.html')
        user_name = request.POST.get('user_name')
        for t in User.objects.all():
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return render(request, 'register_admin.html')
        user = User.objects.create_user(username=user_name, email=email, password=psw)
        user.save()
        t = Registration()
        t.First_name = first_name
        t.Designation = designation
        t.Emp_Id =admin_id
        t.Email = email
        t.location = location
        t.Password = psw
        t.Mobile_Number = mobile_number
        t.Registration_date = z
        t.Gender = gender
        t.Image = photo
        t.Address = useragreement
        t.User_role = admin
        t.user = user
        t.save()
        messages.success(request, 'You have successfully registered as admin')
        return redirect('home')
    else:
        return render(request, 'register_admin.html')



def home(request):
    return render(request,'home.html',)

def logout(request):
    del request.session['logg']
    auth.logout(request)
    if 'logg' in request.session:
        del request.session['logg']
        return redirect('login')
    return redirect('login')


def adminn_details(request):
    bok = Registration.objects.get(id=request.session['logg'])
    gtt = Registration.objects.filter(User_role = 'admin')
    return render(request, "adminn_details.html",{'bok':bok,'gtt':gtt,})



from django.shortcuts import render
from .models import Registration, Attendance
from django.utils.timezone import now

@login_required
@logged_inn4

def employee_home(request):
 # Get the current logged-in user based on the session
    bok = Registration.objects.get(id=request.session['logg'])
    create_pro = CreateProject.objects.all()
    # Get all employees
    gtt = Registration.objects.filter(User_role='employee')
    total_project = CreateProject.objects.count()
    total_timesheet = Create_Timesheet_Line.objects.count()
    total_staffs = Registration.objects.count()
    user = request.user
    leave_balance, _ = LeaveBalance.objects.get_or_create(staff=user)
    total_projects = CreateProject.objects.all()
    # Get the first employee (can be replaced with specific logic)
    df = Registration.objects.filter(User_role='employee').first()

    # Get all Registration records (this is the complete list of employees)
    k = Registration.objects.all()

    # Get the attendance records for the current logged-in user
    attendance_records = Attendance.objects.filter(employee=bok)

    leave_total = LeaveApplication.objects.count()
    leaves = LeaveApplication.objects.filter(staff=bok.user)

    # Count total leaves for the logged-in user
    leave_total = leaves.count()

    # If you need to display total working days and total working hours, you can aggregate that
    total_working_days = attendance_records.count()
    total_working_minutes = sum(
        (att.check_out_time - att.check_in_time).total_seconds() / 60
        for att in Attendance.objects.filter(employee=bok)
        if att.check_in_time and att.check_out_time  # Ensure both times exist
    )


    current_date = now().date()

    open_attendance = Attendance.objects.filter(
        employee=bok,
        date=current_date,
        check_out_time__isnull=True
    ).last()
    context = {
        'k': k,
        'df': df,
        'gtt': gtt,
        'bok': bok,
        'attendance_records': attendance_records,
        'total_working_days': total_working_days,
        'total_working_minutes':  round(total_working_minutes, 2),
        'leave_total':leave_total,
        'leaves':leaves,
        'create_pro':create_pro,
        'total_project':total_project,
        'total_timesheet':total_timesheet,
        'total_staffs':total_staffs,
        'leave_balance':leave_balance,
        'total_projects':total_projects,
        'open_attendance': open_attendance,

    }

    return render(request, 'employee_home.html', context)



from django.shortcuts import render
from .models import Registration

def employeess(request):
    bok = Registration.objects.get(id=request.session['logg'])
    all_users = Registration.objects.filter(User_role='employee')
    return render(request, "employees.html", {'all_users': all_users,'bok':bok})
from datetime import datetime  # Correct import

def register_employee(request):
    bok = Registration.objects.get(id=request.session['logg'])
    if request.method == 'POST':
        x = datetime.now()
        z = x.strftime("%Y-%m-%d")
        emp_id = request.POST.get('emp_id')
        first_name = request.POST.get('first_name')
        designation = request.POST.get('designation')

        mobile_number = request.POST.get('mobile_number')
        email = request.POST.get('email')
        psw = request.POST.get('psw')
        gender = request.POST.get('gender')
        ua = request.POST.get('ua')
        location = request.POST.get('location')
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        fs.save(photo.name, photo)
        employee = request.POST.get('employee')
        reg1 = Registration.objects.all()
        for i in reg1:
            if i.Email == email:
                messages.success(request, 'Employee already Registered')
                return render(request, 'register_employee.html')
        user_name = request.POST.get('user_name')
        for t in User.objects.all():
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return render(request, 'register_employee.html')
        user = User.objects.create_user(username=user_name, email=email, password=psw)
        user.save()
        t = Registration()
        t.Emp_Id = emp_id
        t.First_name = first_name
        t.Designation = designation
        t.Location = location
        t.Email = email
        t.Password = psw
        t.Mobile_Number = mobile_number
        t.Registration_date = z
        t.Gender = gender
        t.Image = photo
        t.Address = ua
        t.User_role = employee
        t.user = user
        t.save()
        messages.success(request, 'Staff Added Successfully')
        return redirect('register_employee')
    else:
        return render(request, 'register_employee.html',{'bok':bok})



from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Registration


def update_employee(request):

    # ✅ Safe session check
    logg = request.session.get('logg')

    if not logg:
        messages.error(request, "Session expired. Please login again.")
        return redirect('login')

    # ✅ Get logged user data
    try:
        reg = Registration.objects.get(id=logg)
        user = User.objects.get(email=reg.Email)
    except Registration.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('login')

    # ✅ POST (Update logic)
    if request.method == 'POST':

        f_name = request.POST.get('first_name')
        designation = request.POST.get('designatio')
        loc = request.POST.get('loc')
        email = request.POST.get('email')
        psw = request.POST.get('psw')
        username = request.POST.get('user_name')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        image = request.FILES.get('photo')

        # ✅ Username validation
        if User.objects.exclude(id=user.id).filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('update_employee')

        # ✅ Update Django User
        user.username = username
        user.email = email

        if psw:
            user.password = make_password(psw)

        user.save()

        # ✅ Update Registration model
        reg.First_name = f_name
        reg.Designation = designation
        reg.Email = email
        reg.Location = loc
        reg.Mobile_Number = mobile
        reg.Address = address
        reg.Gender = gender

        if psw:
            reg.Password = psw   # ⚠️ Avoid storing plain password in production

        if image:
            reg.Image = image

        reg.user = user
        reg.save()

        # ✅ Re-login only if password changed
        if psw:
            user = auth.authenticate(username=username, password=psw)
            if user:
                auth.login(request, user)

        messages.success(request, "Profile Updated Successfully")
        return redirect('update_employee')   # Stay on same page

    # ✅ GET request
    return render(request, 'update_employee.html', {
        'bok': reg,
        'user': user
    })
    
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Registration

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import Registration, User  # Ensure correct model imports
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from .models import Registration  # Adjust import if needed
from django.contrib.auth.models import User  # Assuming you're using default User

from django.contrib.auth.hashers import make_password, check_password

from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from .models import Registration, User
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

def update_employeee(request, employee_id):
    try:
        # Fetch the employee record
        logged_in_user = get_object_or_404(Registration, id=employee_id)
        user_instance = get_object_or_404(User, email=logged_in_user.Email)

        if request.method == 'POST':
            # Get the data from the form
            emp_id = request.POST.get('emp_id')
            first_name = request.POST.get('first_name')
            designation = request.POST.get('designation')
            address = request.POST.get('address')
            email = request.POST.get('email')
            password = request.POST.get('psw')
            photo = request.FILES.get('photo')
            gender = request.POST.get('gender')
            location = request.POST.get('location')
            mobile_number = request.POST.get('mobile_number')
            username = request.POST.get('username')

            # Check if username is already used by another user
            if username and username != user_instance.username:
                if User.objects.filter(username=username).exclude(id=user_instance.id).exists():
                    messages.error(request, 'Username already taken. Please choose another one.')
                    return redirect('update_employeee', employee_id=employee_id)

            # Check if email is already used by another user
            if email and email != user_instance.email:
                if User.objects.filter(email=email).exclude(id=user_instance.id).exists():
                    messages.error(request, 'Email already in use. Please use a different email.')
                    return redirect('update_employeee', employee_id=employee_id)

            # Update User model
            user_instance.email = email
            user_instance.username = username
            if password:
                user_instance.set_password(password)
            user_instance.save()

            # Update Registration model
            logged_in_user.Emp_Id = emp_id
            logged_in_user.First_name = first_name
            logged_in_user.Designation = designation
            logged_in_user.Address = address
            logged_in_user.Email = email
            logged_in_user.Gender = gender
            logged_in_user.Location = location
            logged_in_user.Mobile_Number = mobile_number

            if password:
                logged_in_user.Password = password  # Not recommended to store plain password
            if photo:
                logged_in_user.Image = photo

            logged_in_user.user = user_instance
            logged_in_user.save()

            messages.success(request, 'Employee profile updated successfully!')
            return redirect('view_staffs')

        return render(request, 'update_employeee.html', {'leave': logged_in_user})

    except IntegrityError:
        messages.error(request, 'Database error occurred while updating the profile.')
    except ValidationError as e:
        messages.error(request, f'Validation Error: {e}')
    except Exception as e:
        messages.error(request, f'Error: {e}')

    return redirect('view_staffs')






def del_employee(request, id):
    try:
        employee = get_object_or_404(Registration, id=id)
        user = get_object_or_404(User, email=employee.Email)

        # Delete user and employee records
        user.delete()
        employee.delete()

        messages.success(request, 'Employee account deleted successfully.')
    except Exception as e:
        messages.error(request, f'Error deleting employee: {e}')

    return redirect('view_staffs')


from django.utils.timezone import now
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Attendance, Registration
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from .models import Attendance, Registration

from django.core.files.storage import FileSystemStorage

import base64
import uuid
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404, render
from django.utils.timezone import now
from django.contrib import messages
from .models import Attendance, Registration

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.utils.timezone import now
import uuid
import base64
from .models import Registration, Attendance
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
import base64
import uuid
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from .models import Registration, Attendance  # Import models properly
import uuid
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import Attendance, Registration

def mark_attendance(request):
    bok = get_object_or_404(Registration, id=request.session.get('logg'))
    employee = get_object_or_404(Registration, user=request.user)
    current_datetime = now().replace(microsecond=0)
    current_date = current_datetime.date()

    if request.method == "POST":
        status = request.POST.get("status", "Present")
        fs = FileSystemStorage(location="media/attendance_images/")

        # Fetch today's attendance record
        attendance = Attendance.objects.filter(employee=employee, date=current_date).first()

        if attendance:
            if not attendance.check_out_time:
                attendance.check_out_time = current_datetime

                # Handle check-out image upload
                if "webcamImage" in request.FILES:
                    image_file_out = request.FILES["webcamImage"]
                    image_name_out = f"{uuid.uuid4()}.jpg"
                    attendance.webcam_image_out = fs.save(image_name_out, image_file_out)

                # Calculate total working hours
                attendance.total_working_hours = round(
                    (attendance.check_out_time - attendance.check_in_time).total_seconds() / 3600, 2
                )
                attendance.save()
                messages.success(request, "Successfully logged out")

                # Calculate summary
                total_working_days = Attendance.objects.filter(employee=employee).values("date").distinct().count()
                total_working_hours = round(
                    sum(
                        (att.check_out_time - att.check_in_time).total_seconds() / 3600
                        for att in Attendance.objects.filter(employee=employee)
                        if att.check_in_time and att.check_out_time
                    ),
                    2
                )

                context = {
                    "total_working_days": total_working_days,
                    "total_working_hours": total_working_hours,
                    "bok": bok,
                    "latest_attendance": attendance,
                }
                return render(request, "admin_home_logout.html", context)

            else:
                messages.warning(request, "You have already logged out")
                return render(request, "login.html")

        else:
            # Handle check-in image upload
            webcam_image_in = None
            if "webcamImage" in request.FILES:
                image_file_in = request.FILES["webcamImage"]
                image_name_in = f"{uuid.uuid4()}.jpg"
                webcam_image_in = fs.save(image_name_in, image_file_in)

            # Create a new attendance record
            attendance = Attendance.objects.create(
                employee=employee,
                date=current_date,
                check_in_time=current_datetime,
                status=status,
                webcam_image_in=webcam_image_in,
            )
            messages.success(request, "Welcome Back")

            context = {
                "bok": bok,
                "latest_attendance": attendance,  # Ensure this is passed correctly
            }
            return render(request, "admin_home_login.html", context)

    return render(request, "admin_home.html")


from django.shortcuts import render, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.utils.timezone import now
import uuid

import uuid
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.utils.timezone import now

from .models import Registration, Attendance


from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import uuid

from .models import Attendance, Registration


def mark_attendance_staff(request):

    bok = get_object_or_404(
        Registration,
        id=request.session.get('logg')
    )

    employee = get_object_or_404(
        Registration,
        user=request.user
    )

    current_datetime = now()
    current_date = current_datetime.date()

    fs = FileSystemStorage(location="media/attendance_images/")

    # FIND OPEN ATTENDANCE
    open_attendance = Attendance.objects.filter(
        employee=employee,
        date=current_date,
        check_out_time__isnull=True
    ).last()

    if request.method == "POST":

        status = request.POST.get("status", "Present")
        webcam_image = request.FILES.get("webcamImage")

        # =====================================================
        # CHECK OUT
        # =====================================================
        if open_attendance:

            open_attendance.check_out_time = current_datetime

            # SAVE CHECKOUT IMAGE
            if webcam_image:

                image_name_out = f"{uuid.uuid4()}.jpg"

                open_attendance.webcam_image_out = fs.save(
                    image_name_out,
                    webcam_image
                )

            # CALCULATE HOURS
            total_seconds = (
                open_attendance.check_out_time -
                open_attendance.check_in_time
            ).total_seconds()

            open_attendance.total_working_hours = round(
                total_seconds / 3600,
                2
            )

            open_attendance.save()

            messages.success(
                request,
                "Successfully checked out."
            )

            # TODAY TOTAL HOURS
            total_working_hours = round(
                sum(
                    att.total_working_hours or 0
                    for att in Attendance.objects.filter(
                        employee=employee,
                        date=current_date
                    )
                ),
                2
            )

            context = {
                "bok": bok,
                "latest_attendance": open_attendance,
                "total_working_hours": total_working_hours,
            }

            return render(
                request,
                "employee_home_logout.html",
                context
            )

        # =====================================================
        # CHECK IN
        # =====================================================
        else:

            webcam_image_in = None

            # SAVE CHECKIN IMAGE
            if webcam_image:

                image_name_in = f"{uuid.uuid4()}.jpg"

                webcam_image_in = fs.save(
                    image_name_in,
                    webcam_image
                )

            attendance = Attendance.objects.create(
                employee=employee,
                date=current_date,
                check_in_time=current_datetime,
                status=status,
                webcam_image_in=webcam_image_in,
            )

            messages.success(
                request,
                "Successfully checked in."
            )

            context = {
                "bok": bok,
                "latest_attendance": attendance,
            }

            return render(
                request,
                "employee_home_login.html",
                context
            )

    # =====================================================
    # DEFAULT PAGE
    # =====================================================

    today_attendance = Attendance.objects.filter(
        employee=employee,
        date=current_date
    )

    total_working_hours = round(
        sum(
            att.total_working_hours or 0
            for att in today_attendance
        ),
        2
    )

    context = {
        "bok": bok,
        "open_attendance": open_attendance,
        "today_attendance": today_attendance,
        "total_working_hours": total_working_hours,
    }

    return render(
        request,
        "employee_home.html",
        context
    )




def create_timesheet_staff(request):
    bok = Registration.objects.get(id=request.session['logg'])
    staff_members = Registration.objects.all()
    return render(request, "create_timesheet_staff.html",{'staff_members': staff_members,'bok':bok})

def create_timesheet_admin(request):
    bok = Registration.objects.get(id=request.session['logg'])
    staff_members = Registration.objects.all()
    return render(request, "create_timesheet_admin.html",{'staff_members': staff_members,'bok':bok})

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User  # Assuming you're using the default User model
  # Ensure you import the correct model
from django.shortcuts import render, redirect
from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Create_Timesheet, Create_Timesheet_Line, Registration

from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Registration, Create_Timesheet, Create_Timesheet_Line

from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Registration, Create_Timesheet, Create_Timesheet_Line

from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import make_aware
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import make_aware
from datetime import datetime
from .models import Create_Timesheet, Create_Timesheet_Line, Registration

from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import make_aware
from datetime import datetime
from .models import Registration, Create_Timesheet, Create_Timesheet_Line
from django.contrib.auth.decorators import login_required

@login_required

def add_timesheet_admin(request):
    if request.method == 'POST':
        try:
            # Validate logged-in user
            try:
                admin_user = Registration.objects.get(user=request.user)
            except Registration.DoesNotExist:
                messages.error(request, "Admin user not found.")
                return redirect('create_timesheet_admin')

            # Parse main timesheet date
            date_str = request.POST.get('date')
            if not date_str:
                messages.error(request, "Date is required.")
                return redirect('create_timesheet_admin')

            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                messages.error(request, "Invalid date format. Use DD-MM-YYYY.")
                return redirect('create_timesheet_admin')

            # Create main timesheet entry
            timesheet = Create_Timesheet.objects.create(
                staff_list=admin_user,
                staff_id=admin_user.Emp_Id,
                date=date_obj,
                total_hours_taken=0
            )

            # Collect timesheet line fields
            project_names = request.POST.getlist('project_name')
            project_nos = request.POST.getlist('project_no')
            remarks_list = request.POST.getlist('remarks')
            dates = request.POST.getlist('date')  # multiple dates (one per line)
            total_hours_taken_list = request.POST.getlist('total_hours_taken')

            # Validate all field lengths
            if not all(len(lst) == len(project_names) for lst in [project_nos, remarks_list, dates, total_hours_taken_list]):
                messages.error(request, "Mismatch in input data. Ensure all fields are correctly filled.")
                return redirect('create_timesheet_admin')

            # Create timesheet lines
            for i in range(len(project_names)):
                try:
                    line_date = datetime.strptime(dates[i], '%Y-%m-%d')
                except ValueError:
                    messages.error(request, f"Invalid date format on line {i+1}. Use DD-MM-YYYY.")
                    continue

                Create_Timesheet_Line.objects.create(
                    timesheet=timesheet,
                    staff_list=admin_user,
                    project_name=project_names[i],
                    project_no=project_nos[i],
                    remarks=remarks_list[i],
                    date=line_date,
                    total_hours_taken=total_hours_taken_list[i],
                    duration_hours=0,
                    duration_minutes=0
                )

            messages.success(request, "Timesheet submitted successfully.")
            return redirect('view_timesheets_admin')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('create_timesheet_admin')

    return render(request, 'create_timesheet_admin.html')




from django.contrib.auth.decorators import login_required
from django.utils.timezone import make_aware
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from .models import Create_Timesheet, Create_Timesheet_Line, Registration

@login_required


def add_timesheet_staff(request):
    if request.method == 'POST':
        try:
            # Get the logged-in staff user
            staff_user = Registration.objects.get(user=request.user)

            # Convert date string to a datetime object (add time as midnight)
            date_str = request.POST.get('date')  # Assuming the date is in 'YYYY-MM-DD' format
            if date_str:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            else:
                raise ValueError("Date is required")

            # Create timesheet
            c_t = Create_Timesheet.objects.create(
                staff_list=staff_user,  # Save the staff_user, which is an instance of Registration
                staff_id=staff_user.Emp_Id,
                date=date_obj,  # Use the datetime object here
                total_hours_taken=0  # Default value, can be updated as needed
            )

            # Get multiple timesheet line data
            project_names = request.POST.getlist('project_name')
            project_nos = request.POST.getlist('project_no')
            remarks_list = request.POST.getlist('remarks')
            dates = request.POST.getlist('date')
            total_hours_taken = request.POST.getlist('total_hours_taken')



            # Create timesheet lines
            for index in range(len(project_names)):
                # Convert the date string for each timesheet line to a datetime object
                line_date_str = dates[index]
                line_date_obj = datetime.strptime(line_date_str, '%Y-%m-%d')

                Create_Timesheet_Line.objects.create(
                    timesheet=c_t,
                    staff_list=staff_user,  # Staff info comes from the timesheet instance
                    project_name=project_names[index],
                    project_no=project_nos[index],
                    remarks=remarks_list[index],
                    date=line_date_obj,  # Use the datetime object here
                    total_hours_taken=total_hours_taken[index],
                    duration_hours=0,  # Default value, adjust if needed
                    duration_minutes=0  # Default value, adjust if needed
                )

            messages.success(request, "Timesheet submitted successfully.")
            return redirect('view_timesheets_staff')

        except Registration.DoesNotExist:
            messages.error(request, "Your staff record could not be found.")
        except ValueError:
            messages.error(request, "Invalid date format. Please enter a valid date and time.")
        except Exception as e:
            messages.error(request, f"Error submitting timesheet: {str(e)}")

    return render(request, 'create_timesheet_staff.html')  # Adjust the template name as needed

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required



@login_required
def add_project(request):
    bok = Registration.objects.get(id=request.session['logg'])

    projects = CreateProject.objects.all()
    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        project_no = request.POST.get('project_no')
        remarks = request.POST.get('remarks')
        week_no = request.POST.get('week_no')

        CreateProject.objects.create(
            project_name=project_name,
            project_no=project_no,
            remarks=remarks,
            week_no=week_no
        )
        messages.success(request, 'Project Added successfully.')


        return redirect('add_project')

    return render(request, 'add_project.html',{'projects': projects,'bok':bok})

@login_required
def edit_project(request, project_id):
    bok = Registration.objects.get(id=request.session['logg'])
    project = get_object_or_404(CreateProject, id=project_id)
    if request.method == 'POST':
        project.project_name = request.POST.get('project_name')
        project.project_no = request.POST.get('project_no')
        project.remarks = request.POST.get('remarks')
        project.week_no = request.POST.get('week_no')
        project.save()
        messages.success(request,'Project Updated Successfully')
        return redirect('add_project')

    return render(request, 'edit_project.html', {'project': project,'bok':bok})

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(CreateProject, id=project_id)
    project.delete()
    messages.success(request, 'Project deleted successfully.')
    return redirect('add_project')



# Read Timesheets
# def view_timesheets(request ):
#     bok = Registration.objects.get(id=request.session['logg'])
#     timesheets = Create_Timesheet_Line.objects.all()
#     return render(request, 'view_timesheets.html', {'timesheets': timesheets,'bok':bok})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from datetime import datetime
from .models import Create_Timesheet_Line  # Import your model

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from datetime import datetime
from .models import Create_Timesheet_Line
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Create_Timesheet_Line  # Update with your actual model name

def update_timesheet(request, timesheet_id):
    # Get the timesheet instance
    timesheet = get_object_or_404(Create_Timesheet_Line, id=timesheet_id)

    if request.method == 'POST':
        try:
            # Get and update form data
            project_names = request.POST.getlist('project_name')
            project_nos = request.POST.getlist('project_no')
            remarks_list = request.POST.getlist('remarks')
            dates = request.POST.getlist('date')
            total_hours_taken = request.POST.getlist('total_hours_taken')

            # Ensure lists have the same length
            if not (len(project_names) == len(project_nos) == len(remarks_list) == len(dates) == len(total_hours_taken)):
                messages.error(request, "Mismatch in project details. Please ensure all fields are filled correctly.")
                return redirect('edit_timesheet', timesheet_id=timesheet_id)

            # Update timesheet line
            for index in range(len(project_names)):
                line_date_str = dates[index]
                line_date_obj = datetime.strptime(line_date_str, '%Y-%m-%d')

                # Update the timesheet line with the new values
                timesheet.project_no = project_nos[index]
                timesheet.project_name = project_names[index]
                timesheet.remarks = remarks_list[index]
                timesheet.date = line_date_obj  # Use the datetime object here
                timesheet.total_hours_taken = total_hours_taken[index]

                # Save changes to the database
                timesheet.save()

            messages.success(request, 'Timesheet updated successfully.')
            return redirect('view_timesheets_staff')

        except Exception as e:
            messages.error(request, f'Error updating timesheet: {str(e)}')

    # If GET request, return the form pre-populated with the current timesheet data
    return render(request, 'edit_timesheet.html', {'timesheet': timesheet})


def update_timesheet_admin(request, timesheet_id):
    timesheet = get_object_or_404(Create_Timesheet_Line, id=timesheet_id)

    if request.method == 'POST':
        try:
            # Get and update form data
            project_names = request.POST.getlist('project_name')
            project_nos = request.POST.getlist('project_no')
            remarks_list = request.POST.getlist('remarks')
            dates = request.POST.getlist('date')
            total_hours_taken = request.POST.getlist('total_hours_taken')

            # Ensure lists have the same length
            if not (len(project_names) == len(project_nos) == len(remarks_list) == len(dates) == len(total_hours_taken)):
                messages.error(request, "Mismatch in project details. Please ensure all fields are filled correctly.")
                return redirect('edit_timesheet', timesheet_id=timesheet_id)

            # Update timesheet line
            for index in range(len(project_names)):
                line_date_str = dates[index]
                line_date_obj = datetime.strptime(line_date_str, '%Y-%m-%d')

                # Update the timesheet line with the new values
                timesheet.project_no = project_nos[index]
                timesheet.project_name = project_names[index]
                timesheet.remarks = remarks_list[index]
                timesheet.date = line_date_obj  # Use the datetime object here
                timesheet.total_hours_taken = total_hours_taken[index]

                # Save changes to the database
                timesheet.save()

            messages.success(request, 'Timesheet updated successfully.')
            return redirect('view_timesheets_admin')

        except Exception as e:
            messages.error(request, f'Error updating timesheet: {str(e)}')

    # If GET request, return the form pre-populated with the current timesheet data

    return render(request, 'view_timesheets_admin.html', {'timesheet': timesheet})


# Delete Timesheet
def delete_timesheet_staff(request, timesheet_id):
    timesheet = get_object_or_404(Create_Timesheet_Line, id=timesheet_id)
    timesheet.delete()
    messages.success(request, 'Timesheet deleted successfully.')
    return redirect('view_timesheets_staff')

# Delete Timesheet
def delete_timesheet_staff_all(request, timesheet_id):
    timesheet = get_object_or_404(Create_Timesheet_Line, id=timesheet_id)
    timesheet.delete()
    messages.success(request, 'Timesheet deleted successfully.')
    return redirect('all_view_timesheet_admin')

# Delete Timesheet
def delete_timesheet_admin(request, timesheet_id):
    timesheet = get_object_or_404(Create_Timesheet_Line, id=timesheet_id)
    timesheet.delete()
    messages.success(request, 'Timesheet deleted successfully.')
    return redirect('view_timesheets_admin')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from .models import Registration, LeaveApplication


from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import now
from datetime import datetime
from .models import LeaveApplication, LeaveBalance, ExtraWorkingDay
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from django.utils.timezone import now
from datetime import datetime
from .models import LeaveBalance, LeaveApplication

@login_required
def apply_leave_staff(request):
    bok = Registration.objects.get(id=request.session['logg'])
    user = request.user
    leave_balance, _ = LeaveBalance.objects.get_or_create(staff=user)

    if request.method == 'POST':
        leave_type = request.POST.get('leave_type')
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        reason = request.POST.get('reason')
        document = request.FILES.get('document')

        try:
            date_from_parsed = datetime.strptime(date_from, "%Y-%m-%dT%H:%M")
            date_to_parsed = datetime.strptime(date_to, "%Y-%m-%dT%H:%M")
            delta_days = (date_to_parsed - date_from_parsed).days + 1
            if delta_days <= 0:
                messages.error(request, "End date must be after start date.")
                return redirect('apply_leave_staff')

            current_year = now().year
            used_leaves = LeaveApplication.objects.filter(
                staff=user,
                leave_type=leave_type,
                date_from__year=current_year
            ).aggregate(total=Sum('total_days'))['total'] or 0

            # Leave type logic
            if leave_type == "Casual":
                if used_leaves + delta_days > 12:
                    messages.error(request, f"Annual Casual Leave limit exceeded. Used: {used_leaves}, Max: 12")
                    return redirect('apply_leave_staff')
                if leave_balance.casual_leaves < delta_days:
                    messages.error(request, f"Not enough Casual Leaves. Available: {leave_balance.casual_leaves}")
                    return redirect('apply_leave_staff')
                leave_balance.casual_leaves -= delta_days

            elif leave_type == "Sick":
                if used_leaves + delta_days > 6:
                    messages.error(request, f"Annual Sick Leave limit exceeded. Used: {used_leaves}, Max: 6")
                    return redirect('apply_leave_staff')
                if leave_balance.sick_leaves < delta_days:
                    messages.error(request, f"Not enough Sick Leaves. Available: {leave_balance.sick_leaves}")
                    return redirect('apply_leave_staff')
                leave_balance.sick_leaves -= delta_days

            elif leave_type == "Compensatory":
                if leave_balance.additional_working_days < delta_days:
                    messages.error(request, f"Not enough Additional Working Days. Available: {leave_balance.additional_working_days}")
                    return redirect('apply_leave_staff')
                leave_balance.additional_working_days -= delta_days
                leave_balance.compensatory_leaves -= delta_days  # Optional

            leave_balance.save()

            LeaveApplication.objects.create(
                staff=user,
                leave_type=leave_type,
                date_from=date_from_parsed,
                date_to=date_to_parsed,
                total_days=delta_days,
                reason=reason,
                document=document
            )

            messages.success(request, 'Leave application submitted successfully.')
            return redirect('apply_leave_staff')

        except ValueError:
            messages.error(request, 'Invalid date/time format.')

    return render(request, 'apply_leave_staff.html', {'leave_balance': leave_balance,'bok':bok})
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.timezone import now
from .models import LeaveBalance, AdditionalWorkingDay

def submit_additional_day(request):
    bok = Registration.objects.get(id=request.session['logg'])
    if request.method == 'POST':
        user = request.user
        work_date = request.POST.get('work_date')
        work_reason = request.POST.get('work_reason')

        if work_date and work_reason:
            # Save the additional working day entry
            AdditionalWorkingDay.objects.create(
                staff=user,
                date=work_date,
                reason=work_reason
            )

            # Update LeaveBalance
            leave_balance, _ = LeaveBalance.objects.get_or_create(staff=user)

            # Increment additional working days and reduce compensatory leaves
            leave_balance.additional_working_days += 1

            # Ensure compensatory_leaves doesn't go negative
            if leave_balance.compensatory_leaves > 0:
                leave_balance.compensatory_leaves = max(0, leave_balance.compensatory_leaves - 1)

            leave_balance.save()

            messages.success(request, "Additional working day submitted successfully.")
        else:
            messages.error(request, "Both date and reason are required.")

    return render(request, 'additional_working_day.html',{'bok':bok})

def view_additional_days(request):
    bok = Registration.objects.get(id=request.session['logg'])
    additional_days = AdditionalWorkingDay.objects.filter(staff_id=bok.id)
    return render(request, 'view_additional_days.html', {'additional_days': additional_days,'bok': bok})

def view_additional_days_admin(request):
    bok = Registration.objects.get(id=request.session['logg'])

    additional_days = AdditionalWorkingDay.objects.all()
    return render(request, 'view_additional_days_admin.html', {'additional_days': additional_days,'bok': bok})

def view_additional_days_a(request):
    # Get the logged-in user from the session
    bok = Registration.objects.get(id=request.session['logg'])

    # Filter additional working days related to the logged-in user using the 'staff' field
    additional_days = AdditionalWorkingDay.objects.filter(staff_id=bok.id)


    return render(request, 'view_additional_days_a.html', {
        'additional_days': additional_days,
        'bok': bok
    })




from django.shortcuts import render, redirect
from django.contrib import messages
from .models import AdditionalWorkingDay
from django.utils.dateparse import parse_date
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import AdditionalWorkingDay
from django.utils.dateparse import parse_date
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.dateparse import parse_date
from .models import AdditionalWorkingDay, Registration
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import AdditionalWorkingDay
from django.utils.dateparse import parse_date

def update_additional_day(request, day_id):
    bok = Registration.objects.get(id=request.session['logg'])
    try:
        # Fetch the existing additional working day for the current user
        additional_day = AdditionalWorkingDay.objects.get(id=day_id, staff=request.user)
    except AdditionalWorkingDay.DoesNotExist:
        # Handle case where the record does not exist
        messages.error(request, "Record not found.")
        return redirect('view_additional_days')

    if request.method == 'POST':
        # Retrieve new data from the form
        new_date_str = request.POST.get('work_date')
        new_reason = request.POST.get('work_reason')

        if new_date_str and new_reason:
            new_date = parse_date(new_date_str)
            if not new_date:
                messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
                return render(request, 'update_additional_day.html', {'additional_day': additional_day})

            # Update the entry with the new values
            additional_day.date = new_date
            additional_day.reason = new_reason
            additional_day.save()

            # Success message and redirect to the view page
            messages.success(request, "Entry updated successfully.")
            return redirect('view_additional_days')
        else:
            messages.error(request, "Both date and reason are required.")

    return render(request, 'update_additional_day.html', {'additional_day': additional_day,'bok': bok})

def update_additional_day_a(request, day_id):
    bok = Registration.objects.get(id=request.session['logg'])
    try:
        # Fetch the existing additional working day for the current user
        additional_day = AdditionalWorkingDay.objects.get(id=day_id, staff=request.user)
    except AdditionalWorkingDay.DoesNotExist:
        # Handle case where the record does not exist
        messages.error(request, "Record not found.")
        return redirect('view_additional_days_a')

    if request.method == 'POST':
        # Retrieve new data from the form
        new_date_str = request.POST.get('work_date')
        new_reason = request.POST.get('work_reason')

        if new_date_str and new_reason:
            new_date = parse_date(new_date_str)
            if not new_date:
                messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
                return render(request, 'view_additional_days_a.html', {'additional_day': additional_day})

            # Update the entry with the new values
            additional_day.date = new_date
            additional_day.reason = new_reason
            additional_day.save()

            # Success message and redirect to the view page
            messages.success(request, "Entry updated successfully.")
            return redirect('view_additional_days_a')
        else:
            messages.error(request, "Both date and reason are required.")

    return render(request, 'update_additional_day_a.html', {'additional_day': additional_day,'bok': bok})

from django.contrib import messages
from django.shortcuts import redirect
from .models import AdditionalWorkingDay

def delete_additional_day(request, day_id):
    try:
        # Fetch the additional working day for the current user
        additional_day = AdditionalWorkingDay.objects.get(id=day_id, staff=request.user)
    except AdditionalWorkingDay.DoesNotExist:
        # Handle case where the record does not exist
        messages.error(request, "Record not found.")
        return redirect('view_additional_days')  # Redirect to the view page if the record does not exist

    if request.method == 'POST':
        # If method is POST, perform the deletion
        additional_day.delete()
        messages.success(request, "Entry deleted successfully.")
        return redirect('view_additional_days')

    # If not a POST request, just perform the deletion directly (no confirmation page needed)
    additional_day.delete()
    messages.success(request, "Entry deleted successfully.")
    return redirect('view_additional_days')

def delete_additional_day_a(request, day_id):
    try:
        # Fetch the additional working day for the current user
        additional_day = AdditionalWorkingDay.objects.get(id=day_id, staff=request.user)
    except AdditionalWorkingDay.DoesNotExist:
        # Handle case where the record does not exist
        messages.error(request, "Record not found.")
        return redirect('view_additional_days_a')  # Redirect to the view page if the record does not exist

    if request.method == 'POST':
        # If method is POST, perform the deletion
        additional_day.delete()
        messages.success(request, "Entry deleted successfully.")
        return redirect('view_additional_days_a')

    # If not a POST request, just perform the deletion directly (no confirmation page needed)
    additional_day.delete()
    messages.success(request, "Entry deleted successfully.")
    return redirect('view_additional_days_a')

def submit_additional_day_admin(request):
    bok = Registration.objects.get(id=request.session['logg'])
    if request.method == 'POST':
        user = request.user
        work_date = request.POST.get('work_date')
        work_reason = request.POST.get('work_reason')

        if work_date and work_reason:
            # Save the additional working day entry
            AdditionalWorkingDay.objects.create(
                staff=user,
                date=work_date,
                reason=work_reason
            )

            # Update LeaveBalance
            leave_balance, _ = LeaveBalance.objects.get_or_create(staff=user)

            # Increment additional working days and reduce compensatory leaves
            leave_balance.additional_working_days += 1

            # Ensure compensatory_leaves doesn't go negative
            if leave_balance.compensatory_leaves > 0:
                leave_balance.compensatory_leaves = max(0, leave_balance.compensatory_leaves - 1)

            leave_balance.save()

            messages.success(request, "Additional working day submitted successfully.")
        else:
            messages.error(request, "Both date and reason are required.")

    return render(request, 'additional_working_day_admin.html',{'bok':bok})


@login_required
def add_extra_working_day(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        hours = float(request.POST.get('hours', 8))
        user = request.user

        ExtraWorkingDay.objects.create(staff=user, date=date, hours=hours)

        # Convert hours to full day if >= 8
        if hours >= 8:
            leave_balance, _ = LeaveBalance.objects.get_or_create(staff=user)
            leave_balance.compensatory_leaves += 1
            leave_balance.save()

        messages.success(request, 'Extra working day added and compensatory leave updated.')
        return redirect('dashboard')
    return render(request, 'add_extra_working_day.html')


from datetime import datetime
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import LeaveApplication, Registration  # adjust your imports
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_datetime
from datetime import datetime
from .models import LeaveApplication, Registration
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from datetime import datetime
from .models import LeaveApplication, Registration  # adjust import if needed

@login_required
def apply_leave_admin(request):
    bok = Registration.objects.get(id=request.session['logg'])
    user = request.user
    leave_balance, _ = LeaveBalance.objects.get_or_create(staff=user)

    # Handle the GET request by rendering the form
    if request.method == 'GET':
        return render(request, 'apply_leave_admin.html', {'bok': bok, 'leave_balance': leave_balance})

    # Handle the POST request to apply for leave
    if request.method == 'POST':
        leave_type = request.POST.get('leave_type')
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        reason = request.POST.get('reason')
        document = request.FILES.get('document')

        try:
            date_from_parsed = datetime.strptime(date_from, "%Y-%m-%dT%H:%M")
            date_to_parsed = datetime.strptime(date_to, "%Y-%m-%dT%H:%M")
            delta_days = (date_to_parsed - date_from_parsed).days + 1
            if delta_days <= 0:
                messages.error(request, "End date must be after start date.")
                return redirect('apply_leave_admin')

            current_year = now().year
            used_leaves = LeaveApplication.objects.filter(
                staff=user,
                leave_type=leave_type,
                date_from__year=current_year
            ).aggregate(total=Sum('total_days'))['total'] or 0

            # Leave type logic
            if leave_type == "Casual":
                if used_leaves + delta_days > 12:
                    messages.error(request, f"Annual Casual Leave limit exceeded. Used: {used_leaves}, Max: 12")
                    return redirect('apply_leave_admin')
                if leave_balance.casual_leaves < delta_days:
                    messages.error(request, f"Not enough Casual Leaves. Available: {leave_balance.casual_leaves}")
                    return redirect('apply_leave_admin')
                leave_balance.casual_leaves -= delta_days

            elif leave_type == "Sick":
                if used_leaves + delta_days > 6:
                    messages.error(request, f"Annual Sick Leave limit exceeded. Used: {used_leaves}, Max: 6")
                    return redirect('apply_leave_admin')
                if leave_balance.sick_leaves < delta_days:
                    messages.error(request, f"Not enough Sick Leaves. Available: {leave_balance.sick_leaves}")
                    return redirect('apply_leave_admin')
                leave_balance.sick_leaves -= delta_days

            elif leave_type == "Compensatory":
                if leave_balance.additional_working_days < delta_days:
                    messages.error(request, f"Not enough Additional Working Days. Available: {leave_balance.additional_working_days}")
                    return redirect('apply_leave_admin')
                leave_balance.additional_working_days -= delta_days
                leave_balance.compensatory_leaves -= delta_days  # Optional

            leave_balance.save()

            LeaveApplication.objects.create(
                staff=user,
                leave_type=leave_type,
                date_from=date_from_parsed,
                date_to=date_to_parsed,
                total_days=delta_days,
                reason=reason,
                document=document
            )

            messages.success(request, 'Leave application submitted successfully.')
            return redirect('apply_leave_admin')

        except ValueError:
            messages.error(request, 'Invalid date/time format.')
            return render(request, 'apply_leave_admin.html', {'bok': bok, 'leave_balance': leave_balance})


@login_required
def update_leave_admin(request, leave_id):
    bok = Registration.objects.get(id=request.session['logg'])
    leave = get_object_or_404(LeaveApplication, id=leave_id, staff=request.user)

    leave_balance, _ = LeaveBalance.objects.get_or_create(staff=request.user)

    if request.method == 'POST':
        leave_type = leave.leave_type  # Use the existing leave type for consistency
        datetime_from = request.POST.get('datetime_from')
        datetime_to = request.POST.get('datetime_to')
        reason = request.POST.get('reason')
        document = request.FILES.get('document')

        try:
            if datetime_from and datetime_to:
                date_from_parsed = datetime.strptime(datetime_from, "%Y-%m-%dT%H:%M")
                date_to_parsed = datetime.strptime(datetime_to, "%Y-%m-%dT%H:%M")
                delta_days = (date_to_parsed - date_from_parsed).days + 1

                if delta_days <= 0:
                    messages.error(request, "End date must be after start date.")
                    return redirect('update_leave_admin', leave_id=leave_id)

                current_year = now().year
                used_leaves = LeaveApplication.objects.filter(
                    staff=request.user,
                    leave_type=leave_type,
                    date_from__year=current_year
                ).aggregate(total=Sum('total_days'))['total'] or 0

                # Leave type logic (similar to apply_leave_staff)
                if leave_type == "Casual":
                    if used_leaves + delta_days > 12:
                        messages.error(request, f"Annual Casual Leave limit exceeded. Used: {used_leaves}, Max: 12")
                        return redirect('update_leave_admin', leave_id=leave_id)
                    if leave_balance.casual_leaves < delta_days:
                        messages.error(request, f"Not enough Casual Leaves. Available: {leave_balance.casual_leaves}")
                        return redirect('update_leave_admin', leave_id=leave_id)
                    leave_balance.casual_leaves -= delta_days

                elif leave_type == "Sick":
                    if used_leaves + delta_days > 6:
                        messages.error(request, f"Annual Sick Leave limit exceeded. Used: {used_leaves}, Max: 6")
                        return redirect('update_leave_admin', leave_id=leave_id)
                    if leave_balance.sick_leaves < delta_days:
                        messages.error(request, f"Not enough Sick Leaves. Available: {leave_balance.sick_leaves}")
                        return redirect('update_leave_admin', leave_id=leave_id)
                    leave_balance.sick_leaves -= delta_days

                elif leave_type == "Compensatory":
                    if leave_balance.additional_working_days < delta_days:
                        messages.error(request, f"Not enough Additional Working Days. Available: {leave_balance.additional_working_days}")
                        return redirect('update_leave_admin', leave_id=leave_id)
                    leave_balance.additional_working_days -= delta_days
                    leave_balance.compensatory_leaves -= delta_days  # Optional

                leave_balance.save()

                # Update leave application
                leave.date_from = date_from_parsed
                leave.date_to = date_to_parsed
                leave.total_days = delta_days
                leave.reason = reason
                if document:
                    leave.document = document  # Overwrite if a new file is uploaded
                leave.save()

                messages.success(request, 'Leave application updated successfully.')
                return redirect('view_leaves_admin')
            else:
                messages.error(request, 'Please fill out all fields.')

        except ValueError:
            messages.error(request, 'Invalid date/time format.')

    return render(request, 'view_leaves_admin.html', {'leave': leave, 'bok': bok})


from django.http import HttpResponse, Http404
from django.conf import settings
import os

def download_leave_document(request, leave_id):
    from .models import LeaveApplication
    leave = get_object_or_404(LeaveApplication, id=leave_id, staff=request.user)

    if not leave.document:
        raise Http404("No document attached to this leave application.")

    file_path = os.path.join(settings.MEDIA_ROOT, leave.document.name)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
    else:
        raise Http404("File not found.")


def view_leaves_staff(request):
    bok = Registration.objects.get(id=request.session['logg'])
    leaves = LeaveApplication.objects.filter(staff=bok.user)  # Use the related User instance


    return render(request, 'view_leaves_staff.html', {'leaves': leaves, 'bok': bok})


def view_leaves_admin(request):
    bok = Registration.objects.get(id=request.session['logg'])

    # Filter leaves for the logged-in user
    leaves = LeaveApplication.objects.filter(staff=bok.user) # Change 'user' to the correct foreign key field

    return render(request, 'view_leaves_admin.html', {'leaves': leaves, 'bok': bok})


# Update Leave Application
def update_leave_staff(request, leave_id):
    leave = get_object_or_404(LeaveApplication, id=leave_id)

    if request.method == 'POST':
        leave.date_from = request.POST.get('date_from')
        leave.date_to = request.POST.get('date_to')
        leave.reason = request.POST.get('reason')
        leave.save()
        messages.success(request, 'Leave application updated successfully.')
        return redirect('view_leaves_staff')

    return render(request, 'edit_leave.html', {'leave': leave})


    from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import LeaveApplication  # Adjust if needed
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import LeaveApplication, LeaveBalance
from django.contrib.auth.models import User

def restore_leave_balance(leave):
    try:
        balance = LeaveBalance.objects.get(staff=leave.staff)
        if leave.leave_type == 'Casual':
            balance.casual_leaves += leave.total_days
        elif leave.leave_type == 'Sick':
            balance.sick_leaves += leave.total_days
        elif leave.leave_type == 'Compensatory':
            balance.compensatory_leaves += leave.total_days
        balance.save()
    except LeaveBalance.DoesNotExist:
        # Optionally handle the case where LeaveBalance record is missing
        pass

def delete_leave_staff(request, leave_id):
    leave = get_object_or_404(LeaveApplication, id=leave_id)
    restore_leave_balance(leave)
    leave.delete()
    messages.success(request, 'Leave application deleted successfully.')
    return redirect('view_leaves_staff')

def delete_leave_admin(request, leave_id):
    leave = get_object_or_404(LeaveApplication, id=leave_id)
    restore_leave_balance(leave)
    leave.delete()
    messages.success(request, 'Leave application deleted successfully.')
    return redirect('view_leaves_admin')

def delete_leave_admin_all(request, leave_id):
    leave = get_object_or_404(LeaveApplication, id=leave_id)
    restore_leave_balance(leave)
    leave.delete()
    messages.success(request, 'Leave application deleted successfully.')
    return redirect('view_leaves_admin_all')





from django.shortcuts import get_object_or_404, render
from .models import Create_Timesheet_Line, Create_Timesheet

def view_timesheet(request, timesheet_id):
    bok = Registration.objects.get(id=request.session['logg'])
    # Get the specific timesheet line by ID
    timesheet = get_object_or_404(Create_Timesheet_Line, id=timesheet_id)

    # Fetch related timesheets (You might need to adjust this based on the relationships in your model)
    t = Create_Timesheet.objects.filter(id=timesheet.timesheet_id)  # Example: filter related timesheet by foreign key if applicable
    s = CreateProject.objects.filter(id=timesheet.timesheet_id)
    # Pass the selected timesheet and related timesheets to the template
    return render(request, 'view_timesheet.html', {'timesheet': timesheet, 't': t,'bok':bok,'s':s})


def view_timesheet_admin(request, timesheet_id):
    bok = Registration.objects.get(id=request.session['logg'])
    # Get the specific timesheet line by ID
    timesheet = get_object_or_404(Create_Timesheet_Line, id=timesheet_id)

    # Fetch related timesheets (You might need to adjust this based on the relationships in your model)
    t = Create_Timesheet.objects.filter(id=timesheet.timesheet_id)  # Example: filter related timesheet by foreign key if applicable
    s = CreateProject.objects.filter(id=timesheet.timesheet_id)
    # Pass the selected timesheet and related timesheets to the template
    return render(request, 'view_timesheet_admin.html', {'timesheet': timesheet, 't': t,'bok':bok,'s':s})





from django.http import JsonResponse
from .models import CreateProject

def project_list(request):
    query = request.GET.get('q', '')  # Get search query
    projects = CreateProject.objects.filter(project_no__icontains=query)
    data = [{"project_name": p.project_name, "project_no": p.project_no,"remarks": p.remarks,} for p in projects]
    return JsonResponse(data, safe=False)
from django.shortcuts import get_object_or_404, render
from .models import Create_Timesheet, Registration
from django.shortcuts import render, get_object_or_404
from .models import Create_Timesheet, Registration

from django.shortcuts import render, get_object_or_404
from .models import Create_Timesheet_Line, Registration

def view_timesheets_staff(request):
    # Make sure 'logg' is in session
    staff_id = request.session.get('logg')
    if not staff_id:
        return render(request, 'error.html', {'message': 'User not logged in'})

    # Get the logged-in staff user
    bok = get_object_or_404(Registration, id=staff_id)

    # Fetch timesheet lines linked to this staff
    timesheets = Create_Timesheet_Line.objects.filter(staff_list=bok)

    return render(request, 'view_timesheets_staff.html', {
        'timesheets': timesheets,
        'bok': bok
    })

from collections import defaultdict
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime
from datetime import date, timedelta
from .models import Create_Timesheet_Line, Registration
from collections import defaultdict
from django.shortcuts import render, get_object_or_404
from .models import Registration, Create_Timesheet, Create_Timesheet_Line

from collections import defaultdict
from datetime import timedelta
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from collections import defaultdict
from .models import Create_Timesheet, Create_Timesheet_Line, Registration
from datetime import timedelta
from collections import defaultdict
from django.shortcuts import render, get_object_or_404
from .models import Create_Timesheet, Create_Timesheet_Line, Registration
from datetime import datetime

def get_week_range(date_obj):
    """Return Monday-Sunday date range for a given date."""
    start_of_week = date_obj - timedelta(days=date_obj.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week, end_of_week

def view_all_timesheets(request):
    staff_id = request.session.get('logg')
    if not staff_id:
        return render(request, 'error.html', {'message': 'User not logged in'})

    bok = get_object_or_404(Registration, id=staff_id)


    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')

    timesheets = Create_Timesheet.objects.filter(staff_list=bok)
    timesheet = Create_Timesheet_Line.objects.filter(staff_list=bok)

    if from_date:
        from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
    if to_date:
        to_date = datetime.strptime(to_date, '%Y-%m-%d').date()

    monthly_timesheets = defaultdict(list)
    total_hours_all = 0

    for timesheet in timesheets:
        timesheet_lines = Create_Timesheet_Line.objects.filter(timesheet=timesheet)

        if from_date and to_date:
            timesheet_lines = timesheet_lines.filter(date__range=[from_date, to_date])
        elif from_date:
            timesheet_lines = timesheet_lines.filter(date__gte=from_date)
        elif to_date:
            timesheet_lines = timesheet_lines.filter(date__lte=to_date)

        for entry in timesheet_lines:
            month_label = entry.date.strftime('%b %Y')
            weekday = entry.date.strftime('%a').lower()
            hours = entry.total_hours_taken
            week_no = entry.date.isocalendar()[1]
            week_start, week_end = get_week_range(entry.date)

            hours_by_day = dict.fromkeys(['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'], 0)
            hours_by_day[weekday] = hours

            week_label = f"Week {week_no} ({week_start.strftime('%d-%b-%Y')} to {week_end.strftime('%d-%b-%Y')})"

            monthly_timesheets[month_label].append({
                'id': entry.id,
                'project_no': entry.project_no,
                'project_name': entry.project_name,
                'remarks': entry.remarks,
                'hours': hours_by_day,
                'total': hours,
                'week_label': week_label,
                'date': entry.date,  # ✅ ADD THIS LINE
            })


            total_hours_all += hours

    return render(request, 'view_all_timesheets.html', {
        'monthly_timesheets': dict(monthly_timesheets),
        'total_hours': total_hours_all,
        'bok': bok,
        'from_date': from_date,
        'to_date': to_date,
        'timesheet':timesheet
    })





from collections import defaultdict
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from .models import Registration, Create_Timesheet, Create_Timesheet_Line


def view_all_timesheets_admin(request):
    staff_id = request.session.get('logg')
    if not staff_id:
        return render(request, 'error.html', {'message': 'User not logged in'})

    bok = get_object_or_404(Registration, id=staff_id)

    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')

    timesheets = Create_Timesheet.objects.all()

    if from_date:
        from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
    if to_date:
        to_date = datetime.strptime(to_date, '%Y-%m-%d').date()

    monthly_timesheets = defaultdict(list)
    total_hours_all = 0

    for timesheet in timesheets:
        timesheet_lines = Create_Timesheet_Line.objects.filter(timesheet=timesheet)

        if from_date and to_date:
            timesheet_lines = timesheet_lines.filter(date__range=[from_date, to_date])
        elif from_date:
            timesheet_lines = timesheet_lines.filter(date__gte=from_date)
        elif to_date:
            timesheet_lines = timesheet_lines.filter(date__lte=to_date)

        for entry in timesheet_lines:
            month_label = entry.date.strftime('%b %Y')
            weekday = entry.date.strftime('%a').lower()
            hours = entry.total_hours_taken
            week_no = entry.date.isocalendar()[1]
            week_start, week_end = get_week_range(entry.date)

            hours_by_day = dict.fromkeys(['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'], 0)
            hours_by_day[weekday] = hours

            week_label = f"Week {week_no} ({week_start.strftime('%d-%b-%Y')} to {week_end.strftime('%d-%b-%Y')})"

            monthly_timesheets[month_label].append({
                'id': entry.id,
                'project_no': entry.project_no,
                'project_name': entry.project_name,
                'remarks': entry.remarks,
                'hours': hours_by_day,
                'total': hours,
                'week_label': week_label,
                'date': entry.date,
                'staff_name': entry.staff_list.First_name if entry.staff_list else "N/A",  # ✅ per entry
            })

            total_hours_all += hours

    return render(request, 'view_all_timesheets_admin.html', {
        'monthly_timesheets': dict(monthly_timesheets),
        'total_hours': total_hours_all,
        'bok': bok,
        'from_date': from_date,
        'to_date': to_date,
    })

from collections import defaultdict
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from .models import Create_Timesheet, Create_Timesheet_Line, Registration

def view_all_timesheets_admins(request):
    staff_id = request.session.get('logg')
    if not staff_id:
        return render(request, 'error.html', {'message': 'User not logged in'})

    bok = get_object_or_404(Registration, id=staff_id)

    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')

    # Convert dates if provided
    if from_date:
        from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
    if to_date:
        to_date = datetime.strptime(to_date, '%Y-%m-%d').date()

    monthly_timesheets = defaultdict(list)
    total_hours_all = 0

    # Get all timesheets
    timesheets = Create_Timesheet.objects.all()

    for timesheet in timesheets:
        timesheet_lines = Create_Timesheet_Line.objects.filter(timesheet=timesheet)

        if from_date and to_date:
            timesheet_lines = timesheet_lines.filter(date__range=[from_date, to_date])
        elif from_date:
            timesheet_lines = timesheet_lines.filter(date__gte=from_date)
        elif to_date:
            timesheet_lines = timesheet_lines.filter(date__lte=to_date)

        # Process each entry of the timesheet
        for entry in timesheet_lines:
            month_label = entry.date.strftime('%b %Y')  # Month and Year
            weekday = entry.date.strftime('%a').lower()  # Weekday
            hours = entry.total_hours_taken  # Hours worked on the entry
            week_no = entry.date.isocalendar()[1]  # Week number
            week_start, week_end = get_week_range(entry.date)  # Get week range

            # Create dictionary for hours by day
            hours_by_day = dict.fromkeys(['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'], 0)
            hours_by_day[weekday] = hours  # Assign hours to the respective day

            # Week label
            week_label = f"Week {week_no} ({week_start.strftime('%d-%b-%Y')} to {week_end.strftime('%d-%b-%Y')})"

            # Add the entry to the monthly_timesheets
            monthly_timesheets[month_label].append({
                'id': entry.id,
                'project_no': entry.project_no,
                'project_name': entry.project_name,
                'remarks': entry.remarks,
                'hours': hours_by_day,
                'total': hours,  # Total hours worked for this entry
                'week_label': week_label,
                'date': entry.date,
                'staff_name': entry.staff_list.First_name if entry.staff_list else "N/A",  # Staff Name
                'staff_id': entry.staff_list.id if entry.staff_list else None,  # Staff ID
                'total_hours_taken': entry.total_hours_taken,  # Total hours for this entry
            })

            total_hours_all += hours  # Accumulate total hours

    # Pass the context to the template
    return render(request, 'view_all_timesheets_admins.html', {
        'monthly_timesheets': dict(monthly_timesheets),
        'total_hours': total_hours_all,
        'bok': bok,
        'from_date': from_date,
        'to_date': to_date,
    })


from django.db.models import Sum
from django.shortcuts import render
from .models import Create_Timesheet_Line

def summary_view(request):
    timesheet_data = Create_Timesheet_Line.objects.values('project_no', 'staff_name')\
        .annotate(total_hours=Sum('hours'))\
        .order_by('project_no', 'staff_name')

    # Get unique staff and projects
    staff_names = sorted(set(row['staff_name'] for row in timesheet_data))
    projects = sorted(set(row['project_no'] for row in timesheet_data))

    # Build a dict: {project_no: {staff_name: hours}}
    project_summary = {project: {staff: 0 for staff in staff_names} for project in projects}
    for row in timesheet_data:
        project_summary[row['project_no']][row['staff_name']] = row['total_hours']

    context = {
        'staff_names': staff_names,
        'project_summary': project_summary,
    }

    return render(request, 'view_all_timesheets_admins.html', context)

def view_timesheets_admin(request):
    bok = get_object_or_404(Registration, id=request.session.get('logg'))
    timesheets = Create_Timesheet_Line.objects.filter(staff_list_id=bok.id)
    return render(request, 'view_timesheets_admin.html', {'timesheets': timesheets, 'bok': bok})

def view_staffs(request):
    bok = get_object_or_404(Registration, id=request.session.get('logg'))
    view_s =  Registration.objects.filter(User_role = 'employee')
    return render(request, 'view_staffs.html',{'view_s':view_s,'bok':bok} )

def view_staff_details(request, id):
    bok = get_object_or_404(Registration, id=request.session.get('logg'))
    leave = get_object_or_404(Registration, id=id)

    # Fetch records related to the specific leave/registration user
    registrations = Registration.objects.filter(id=leave.id)
    timesheets = Create_Timesheet.objects.filter(staff_list_id=bok.id) # Assuming 'user' field relates to Registration
    timesheet_lines = Create_Timesheet_Line.objects.filter(staff_list_id=bok.id)  # Assuming 'timesheet' is related to the user
    attendance_records = Attendance.objects.filter(employee=bok.id) # Assuming 'user' field in Attendance model
    leave_applications = LeaveApplication.objects.filter(staff=bok.id)  # Assuming 'user' field in LeaveApplication model
    projects = CreateProject.objects.filter(id=id) # Assuming 'users' is a many-to-many relation with Registration

    return render(request, 'view_staff_details.html', {
        'bok': bok,
        'registrations': registrations,
        'timesheets': timesheets,
        'timesheet_lines': timesheet_lines,
        'attendance_records': attendance_records,
        'leave_applications': leave_applications,
        'projects': projects,
    })





def view_staff_detail(request, id):
    bok = get_object_or_404(Registration, id=request.session.get('logg'))
    leave = get_object_or_404(Registration, id=id)

    # Fetch records related to the specific leave/registration user
    registrations = Registration.objects.filter(id=leave.id)
    timesheets = Create_Timesheet.objects.filter(staff_list_id=bok.id) # Assuming 'user' field relates to Registration
    timesheet_lines = Create_Timesheet_Line.objects.filter(staff_list_id=leave.id)  # Assuming 'timesheet' is related to the user
    attendance_records = Attendance.objects.filter(employee=bok.id) # Assuming 'user' field in Attendance model
    leave_applications = LeaveApplication.objects.filter(staff=bok.id)  # Assuming 'user' field in LeaveApplication model
    projects = CreateProject.objects.filter(id=id) # Assuming 'users' is a many-to-many relation with Registration
    all_timesheet = Create_Timesheet_Line.objects.all()


    # Define `timesheet` before using it
    if all_timesheet.exists():  # Ensure there's at least one timesheet
        timesheet = all_timesheet.first()  # Get the first timesheet line
        t = Create_Timesheet.objects.filter(id=timesheet.timesheet_id)
    else:
        t = Create_Timesheet.objects.none()  # Return an empty queryset if no timesheets exist

    return render(request, 'view_staff_detail.html', {
        'bok': bok,
        'registrations': registrations,
        'timesheets': timesheets,
        'timesheet_lines': timesheet_lines,
        'attendance_records': attendance_records,
        'leave_applications': leave_applications,
        'projects': projects,
        'all_timesheet':all_timesheet

    })


from django.http import JsonResponse
from .models import Create_Timesheet_Line, Registration

def get_staff_by_project(request):
    project_no = request.GET.get('project_no')

    # Adjust the filtering logic as per your real data structure
    timesheet_lines = Create_Timesheet_Line.objects.filter(project_no=project_no)
    staff = Registration.objects.filter(timesheet_lines__in=timesheet_lines).distinct()

    staff_data = [{"id": s.id, "name": str(s)} for s in staff]  # Adjust name if needed
    return JsonResponse({"staff": staff_data})


from django.shortcuts import render
from .models import Create_Timesheet_Line
from django.shortcuts import render
from .models import Create_Timesheet_Line

from django.shortcuts import render
from .models import Create_Timesheet_Line
from django.shortcuts import get_object_or_404

def worked_staffs(request, project_id):
    bok = get_object_or_404(Registration, id=request.session.get('logg'))
    # Get the project object by ID
    project = get_object_or_404(CreateProject, id=project_id)

    # Filter timesheet lines by matching project_no
    timesheet_lines = Create_Timesheet_Line.objects.filter(project_no=project.project_no)

    return render(request, 'worked_staffs.html', {
        'timesheet_lines': timesheet_lines,
        'project': project,
        'bok':bok
    })




def view_leaves_admin_all(request):
    bok = Registration.objects.get(id=request.session['logg'])

    # Filter leaves for the logged-in user
    leaves = LeaveApplication.objects.all()# Change 'user' to the correct foreign key field

    return render(request, 'view_leaves_admin_all.html', {'leaves': leaves, 'bok': bok})


# core/views.py

from django.shortcuts import render

def custom_404(request, exception):
    return render(request, 'errors/404.html', status=404)

def custom_500(request):
    return render(request, 'errors/500.html', status=500)

def custom_403(request, exception):
    return render(request, 'errors/403.html', status=403)

def custom_400(request, exception):
    return render(request, 'errors/400.html', status=400)

from django.shortcuts import render
from .models import Attendance, Registration  # Make sure Registration is imported

def view_attendance(request):
    bok = Registration.objects.get(id=request.session['logg'])

    # Show only attendance for the logged-in employee
    attendance = Attendance.objects.all()

    return render(request, 'view_attendance.html', {
        'attendance': attendance,
        'bok': bok
    })








def services(request):

    return render(request, 'services.html', {

    })


def careers(request):

    return render(request, 'careers.html', {

    })


def about(request):

    return render(request, 'about.html', {

    })
def contactus(request):

    return render(request, 'contactus.html', {

    })
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render
from django.conf import settings

def contact_view(request):
    context = {}

    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        # Validation
        if not name or not email or not subject or not message:
            context['error'] = "All fields are required."
            return render(request, 'contactus.html', context)

        full_message = f"""
Name: {name}
Email: {email}

Message:
{message}
"""

        try:
            send_mail(
                subject=subject,
                message=full_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['codexlertechnologies@gmail.com'],
                fail_silently=False,
            )
            context['success'] = "Your message has been sent successfully!"

        except BadHeaderError:
            context['error'] = "Invalid header found."

        except Exception as e:
            print("EMAIL ERROR:", e)  # 👈 VERY IMPORTANT for debugging
            context['error'] = "Something went wrong. Please try again later."

    return render(request, 'contactus.html', context)


from django.shortcuts import render

# ================= SERVICES PAGES =================

def web_development(request):
    return render(request, 'services/web_development.html')


def mobile_apps(request):
    return render(request, 'services/mobile_apps.html')


def digital_marketing(request):
    return render(request, 'services/digital_marketing.html')


def custom_software(request):
    return render(request, 'services/custom_software.html')


def ai_solutions(request):
    return render(request, 'services/ai_solutions.html')


def cloud_solutions(request):
    return render(request, 'services/cloud_solutions.html')




def expense_list(request):
    expenses = Expense.objects.all().order_by('-date')

    # GET filters
    category_id = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if category_id:
        expenses = expenses.filter(category_id=category_id)

    if start_date:
        expenses = expenses.filter(date__gte=start_date)

    if end_date:
        expenses = expenses.filter(date__lte=end_date)

    categories = ExpenseCategory.objects.all()

    total = expenses.aggregate(Sum('amount'))['amount__sum']

    return render(request, 'expenses_list.html', {
        'expenses': expenses,
        'categories': categories,
        'total': total
    })


def add_expense(request):

    categories = ExpenseCategory.objects.all()

    if request.method == "POST":
        category_id = request.POST.get('category')
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        description = request.POST.get('description')
        receipt = request.FILES.get('receipt')

        category = ExpenseCategory.objects.get(id=category_id)

        Expense.objects.create(
            category=category,
            amount=amount,
            date=date,
            description=description,
            receipt=receipt
        )
        return redirect('expense_list')

    return render(request, 'expenses_add.html', {'categories': categories})


def edit_expense(request, id):


    expense = get_object_or_404(Expense, id=id)
    categories = ExpenseCategory.objects.all()

    if request.method == "POST":
        category_id = request.POST.get('category')
        expense.category = ExpenseCategory.objects.get(id=category_id)
        expense.amount = request.POST.get('amount')
        expense.date = request.POST.get('date')
        expense.description = request.POST.get('description')

        if request.FILES.get('receipt'):
            expense.receipt = request.FILES.get('receipt')

        expense.save()
        return redirect('expense_list')

    return render(request, 'expenses_edit.html', {
        'expense': expense,
        'categories': categories
    })


def delete_expense(request, id):


    expense = get_object_or_404(Expense, id=id)
    expense.delete()
    return redirect('expense_list')

def category_list(request):


    categories = ExpenseCategory.objects.all()
    return render(request, 'category_list.html', {'categories': categories})


def add_category(request):


    if request.method == "POST":
        name = request.POST.get('name')

        if name:   # basic validation
            ExpenseCategory.objects.create(name=name)

        return redirect('category_list')

    return render(request, 'add_category.html')


def edit_category(request, id):


    category = get_object_or_404(ExpenseCategory, id=id)

    if request.method == "POST":
        name = request.POST.get('name')

        if name:
            category.name = name
            category.save()

        return redirect('category_list')

    return render(request, 'edit_category.html', {'category': category})


def delete_category(request, id):

    category = get_object_or_404(ExpenseCategory, id=id)
    category.delete()

    return redirect('category_list')


import openpyxl
from django.http import HttpResponse
from .models import Expense


def export_excel(request):


    expenses = Expense.objects.all().order_by('-date')

    # 🔍 Apply same filters
    category_id = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if category_id:
        expenses = expenses.filter(category_id=category_id)

    if start_date:
        expenses = expenses.filter(date__gte=start_date)

    if end_date:
        expenses = expenses.filter(date__lte=end_date)

    # 📄 Create Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Expenses"

    # Header
    headers = ["Category", "Amount", "Date", "Description"]
    ws.append(headers)

    # Data
    for e in expenses:
        ws.append([
            e.category.name,
            float(e.amount),
            str(e.date),
            e.description
        ])

    # Response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=expenses.xlsx'

    wb.save(response)
    return response

from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from collections import defaultdict
from calendar import month_abbr
from datetime import date
@login_required
@logged_inn6
def f_dashboard(request):

    # ==================================
    # TOTAL INCOME
    # ==================================

    total_income = (
        Income.objects.aggregate(
            total=Sum('amount')
        )['total'] or 0
    )


    # ==================================
    # GENERAL EXPENSE
    # ==================================

    general_expense = (
        Expense.objects.aggregate(
            total=Sum('amount')
        )['total'] or 0
    )


    # ==================================
    # PROJECT EXPENSE
    # ==================================

    project_expense = (
        ProjectExpense.objects.aggregate(
            total=Sum('amount')
        )['total'] or 0
    )


    # ==================================
    # TOTAL EXPENSE
    # ==================================

    total_expense = (
        general_expense +
        project_expense
    )


    # ==================================
    # NET BALANCE
    # ==================================

    net_balance = (
        total_income -
        total_expense
    )


    # ==================================
    # MONTHLY CHART DATA
    # ==================================

    income_chart = defaultdict(int)

    expense_chart = defaultdict(int)


    # -------------------------------
    # INCOME CHART
    # -------------------------------

    income_data = Income.objects.annotate(
        month=ExtractMonth('date')
    ).values('month').annotate(
        total=Sum('amount')
    )

    for item in income_data:

        income_chart[item['month']] = float(
            item['total']
        )


    # -------------------------------
    # EXPENSE CHART
    # -------------------------------

    expense_data = Expense.objects.annotate(
        month=ExtractMonth('date')
    ).values('month').annotate(
        total=Sum('amount')
    )

    for item in expense_data:

        expense_chart[item['month']] += float(
            item['total']
        )


    # -------------------------------
    # PROJECT EXPENSE CHART
    # -------------------------------

    project_expense_data = ProjectExpense.objects.annotate(
        month=ExtractMonth('date')
    ).values('month').annotate(
        total=Sum('amount')
    )

    for item in project_expense_data:

        expense_chart[item['month']] += float(
            item['total']
        )


    # ==================================
    # CHART LABELS
    # ==================================

    labels = []

    income_values = []

    expense_values = []

    for i in range(1, 13):

        labels.append(
            month_abbr[i]
        )

        income_values.append(
            income_chart[i]
        )

        expense_values.append(
            expense_chart[i]
        )


    # ==================================
    # RECENT TRANSACTIONS
    # ==================================

    transactions = []


    # -------------------------------
    # INCOME
    # -------------------------------

    for i in Income.objects.all():

        transactions.append({

            'date': i.date,

            'type': 'Income',

            'category': (
                i.source
                if i.source
                else 'Income'
            ),

            'amount': i.amount

        })


    # -------------------------------
    # EXPENSE
    # -------------------------------

    for e in Expense.objects.all():

        transactions.append({

            'date': e.date,

            'type': 'Expense',

            'category': (
                e.category.name
                if e.category
                else 'Expense'
            ),

            'amount': e.amount

        })


    # -------------------------------
    # SORT
    # -------------------------------

    transactions = sorted(
        transactions,
        key=lambda x: x['date'],
        reverse=True
    )[:5]


    # ==================================
    # CONTEXT
    # ==================================

    context = {

        'today': date.today(),

        'total_income': total_income,

        'general_expense': general_expense,

        'project_expense': project_expense,

        'total_expense': total_expense,

        'net_balance': net_balance,

        'labels': labels,

        'income_values': income_values,

        'expense_values': expense_values,

        'transactions': transactions,

    }

    return render(
        request,
        'f_dashboard.html',
        context
    )

def client_payments(request):
    if request.method == "POST":
        client_id = request.POST.get("client")
        project_id = request.POST.get("project")
        amount = request.POST.get("amount")
        date = request.POST.get("date")
        payment_mode = request.POST.get("payment_mode")

        Income.objects.create(
            type='client',
            client_id=client_id,
            project_id=project_id,
            amount=amount,
            date=date,
            payment_mode=payment_mode
        )

        return redirect('client_payments')

    incomes = Income.objects.filter(type='client').order_by('-date')
    clients = Client.objects.all()
    projects = Project.objects.all()

    return render(request, 'client_payments.html', {
        'incomes': incomes,
        'clients': clients,
        'projects': projects
    })


# -------------------------------
# OTHER INCOME
# -------------------------------
def other_income(request):
    if request.method == "POST":
        source = request.POST.get("source")
        amount = request.POST.get("amount")
        date = request.POST.get("date")

        Income.objects.create(
            type='other',
            source=source,
            amount=amount,
            date=date
        )

        return redirect('other_income')

    incomes = Income.objects.filter(type='other').order_by('-date')

    return render(request, 'other_income.html', {
        'incomes': incomes
    })


# -------------------------------
# RECURRING INCOME
# -------------------------------
def recurring_income(request):
    if request.method == "POST":
        source = request.POST.get("source")
        amount = request.POST.get("amount")
        frequency = request.POST.get("frequency")
        date = request.POST.get("date")

        Income.objects.create(
            type='recurring',
            source=source,
            amount=amount,
            frequency=frequency,
            date=date
        )

        return redirect('recurring_income')

    incomes = Income.objects.filter(type='recurring').order_by('-date')

    return render(request, 'recurring_income.html', {
        'incomes': incomes
    })

def client_list(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        company = request.POST.get("company")

        Client.objects.create(
            name=name,
            email=email,
            phone=phone,
            company=company
        )
        return redirect('client_list')

    clients = Client.objects.all()
    return render(request, 'client_list.html', {'clients': clients})

def delete_client(request, id):
    client = get_object_or_404(Client, id=id)
    client.delete()
    return redirect('client_list')


def projects(request):
    if request.method == "POST":
        name = request.POST.get("name")
        client_id = request.POST.get("client")
        amount = request.POST.get("amount")

        Project.objects.create(
            name=name,
            client_id=client_id,
            total_amount=amount
        )
        return redirect('projects')

    projects = Project.objects.all()
    clients = Client.objects.all()

    return render(request, 'projects.html', {
        'projects': projects,
        'clients': clients
    })

def project_income(request):

    if request.method == "POST":
        project_id = request.POST.get("project")
        amount = request.POST.get("amount")
        date = request.POST.get("date")
        notes = request.POST.get("notes")

        ProjectIncome.objects.create(
            project_id=project_id,
            amount=amount,
            date=date,
            notes=notes
        )

        return redirect('project_income')

    projects = Project.objects.all()
    incomes = ProjectIncome.objects.all().order_by('-date')

    return render(request, 'project_income.html', {
        'projects': projects,
        'incomes': incomes
    })


def project_expenses(request):

    if request.method == "POST":
        project_id = request.POST.get("project")
        expense_name = request.POST.get("expense_name")
        amount = request.POST.get("amount")
        date = request.POST.get("date")

        ProjectExpense.objects.create(
            project_id=project_id,
            expense_name=expense_name,
            amount=amount,
            date=date
        )

        return redirect('project_expenses')

    projects = Project.objects.all()
    expenses = ProjectExpense.objects.all().order_by('-date')

    return render(request, 'project_expenses.html', {
        'projects': projects,
        'expenses': expenses
    })


def project_profit(request):

    projects = Project.objects.all()

    project_data = []

    for p in projects:

        total_income = ProjectIncome.objects.filter(
            project=p
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        total_expense = ProjectExpense.objects.filter(
            project=p
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        profit = total_income - total_expense

        project_data.append({
            'project': p,
            'income': total_income,
            'expense': total_expense,
            'profit': profit
        })

    return render(request, 'project_profit.html', {
        'project_data': project_data
    })

from django.db.models import Sum


def payment_history(request):

    incomes = Income.objects.filter(
        type='client'
    ).order_by('-date')

    return render(request, 'payment_history.html', {
        'incomes': incomes
    })

def pending_payments(request):

    projects = Project.objects.all()

    pending_data = []

    for p in projects:

        total_paid = Income.objects.filter(
            project=p,
            type='client'
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        pending = p.total_amount - total_paid

        pending_data.append({
            'project': p,
            'client': p.client,
            'total_amount': p.total_amount,
            'paid': total_paid,
            'pending': pending
        })

    return render(request, 'pending_payments.html', {
        'pending_data': pending_data
    })


def transactions(request):

    incomes = Income.objects.all()

    expenses = Expense.objects.all()

    project_expenses = ProjectExpense.objects.all()

    transaction_list = []

    # Income Transactions
    for i in incomes:

        transaction_list.append({
            'date': i.date,
            'type': 'Income',
            'category': i.type,
            'description': i.source if i.source else (
                i.project.name if i.project else '-'
            ),
            'amount': i.amount,
            'transaction_type': 'credit'
        })

    # Expense Transactions
    for e in expenses:

        transaction_list.append({
            'date': e.date,
            'type': 'Expense',
            'category': e.category.name if e.category else '-',
            'description': e.description,
            'amount': e.amount,
            'transaction_type': 'debit'
        })

    # Project Expense Transactions
    for pe in project_expenses:

        transaction_list.append({
            'date': pe.date,
            'type': 'Project Expense',
            'category': pe.project.name,
            'description': pe.expense_name,
            'amount': pe.amount,
            'transaction_type': 'debit'
        })

    # Sort by latest date
    transaction_list = sorted(
        transaction_list,
        key=lambda x: x['date'],
        reverse=True
    )

    return render(request, 'transactions.html', {
        'transactions': transaction_list
    })


def profit_loss(request):

    # -----------------------
    # TOTAL INCOME
    # -----------------------

    total_income = Income.objects.aggregate(
        Sum('amount')
    )['amount__sum'] or 0


    # -----------------------
    # TOTAL EXPENSE
    # -----------------------

    expense_total = Expense.objects.aggregate(
        Sum('amount')
    )['amount__sum'] or 0

    project_expense_total = ProjectExpense.objects.aggregate(
        Sum('amount')
    )['amount__sum'] or 0

    total_expense = expense_total + project_expense_total


    # -----------------------
    # NET PROFIT
    # -----------------------

    net_profit = total_income - total_expense


    return render(request, 'profit_loss.html', {

        'total_income': total_income,

        'total_expense': total_expense,

        'net_profit': net_profit,

        'expense_total': expense_total,

        'project_expense_total': project_expense_total

    })



def cash_flow(request):

    # -------------------------
    # TOTAL CASH IN
    # -------------------------

    total_income = Income.objects.aggregate(
        Sum('amount')
    )['amount__sum'] or 0


    # -------------------------
    # TOTAL CASH OUT
    # -------------------------

    general_expense = Expense.objects.aggregate(
        Sum('amount')
    )['amount__sum'] or 0

    project_expense = ProjectExpense.objects.aggregate(
        Sum('amount')
    )['amount__sum'] or 0

    total_outflow = general_expense + project_expense


    # -------------------------
    # NET CASH FLOW
    # -------------------------

    net_cash_flow = total_income - total_outflow


    return render(request, 'cash_flow.html', {

        'total_income': total_income,

        'general_expense': general_expense,

        'project_expense': project_expense,

        'total_outflow': total_outflow,

        'net_cash_flow': net_cash_flow

    })
from django.db.models.functions import ExtractMonth
from calendar import month_name
import csv
def monthly_report(request):

    monthly_data = defaultdict(lambda: {
        'income': 0,
        'expense': 0
    })

    # -------------------------
    # INCOME
    # -------------------------

    income_data = Income.objects.annotate(
        month=ExtractMonth('date')
    ).values('month').annotate(
        total=Sum('amount')
    )

    for item in income_data:

        month = item['month']

        monthly_data[month]['income'] = item['total']


    # -------------------------
    # GENERAL EXPENSE
    # -------------------------

    expense_data = Expense.objects.annotate(
        month=ExtractMonth('date')
    ).values('month').annotate(
        total=Sum('amount')
    )

    for item in expense_data:

        month = item['month']

        monthly_data[month]['expense'] += item['total']


    # -------------------------
    # PROJECT EXPENSE
    # -------------------------

    project_expense_data = ProjectExpense.objects.annotate(
        month=ExtractMonth('date')
    ).values('month').annotate(
        total=Sum('amount')
    )

    for item in project_expense_data:

        month = item['month']

        monthly_data[month]['expense'] += item['total']


    # -------------------------
    # FINAL REPORT
    # -------------------------

    report = []

    for month, values in monthly_data.items():

        income = values['income']

        expense = values['expense']

        profit = income - expense

        report.append({
            'month': month_name[month],
            'income': income,
            'expense': expense,
            'profit': profit
        })


    # -------------------------
    # SORT
    # -------------------------

    report = sorted(
        report,
        key=lambda x: list(month_name).index(x['month'])
    )


    # -------------------------
    # EXPORT CSV
    # -------------------------

    if request.GET.get('export') == 'csv':

        response = HttpResponse(content_type='text/csv')

        response['Content-Disposition'] = (
            'attachment; filename="monthly_report.csv"'
        )

        writer = csv.writer(response)

        writer.writerow([
            'Month',
            'Income',
            'Expense',
            'Profit/Loss'
        ])

        for r in report:

            writer.writerow([
                r['month'],
                r['income'],
                r['expense'],
                r['profit']
            ])

        return response


    return render(request, 'monthly_report.html', {
        'report': report
    })

def register_accounts(request):
    if request.method == 'POST':
        x = datetime.now()
        z = x.strftime("%Y-%m-%d")
        admin_id = request.POST.get('admin_id')
        first_name = request.POST.get('first_name')
        designation = request.POST.get('designation')
        location = request.POST.get('location')

        mobile_number = request.POST.get('mobile_number')
        email = request.POST.get('email')
        psw = request.POST.get('psw')
        gender = request.POST.get('gender')
        useragreement = request.POST.get('useragreement')
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        fs.save(photo.name, photo)
        admin = request.POST.get('adminn1')
        reg1 = Registration.objects.all()
        for i in reg1:
            if i.Email == email:
                messages.success(request, 'User already exists')
                return render(request, 'register_accounts.html')
        user_name = request.POST.get('user_name')
        for t in User.objects.all():
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return render(request, 'register_accounts.html')
        user = User.objects.create_user(username=user_name, email=email, password=psw)
        user.save()
        t = Registration()
        t.First_name = first_name
        t.Designation = designation
        t.Emp_Id =admin_id
        t.Email = email
        t.location = location
        t.Password = psw
        t.Mobile_Number = mobile_number
        t.Registration_date = z
        t.Gender = gender
        t.Image = photo
        t.Address = useragreement
        t.User_role = admin
        t.user = user
        t.save()
        messages.success(request, 'You have successfully registered as Accounts')
        return redirect('home')
    else:
        return render(request, 'register_accounts.html')



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from django.utils.timezone import now
from decimal import Decimal
import calendar

from .models import *


# ==========================================
# Salary Structure List
# ==========================================
def salary_structure_list(request):

    bok = Registration.objects.get(id=request.session['logg'])

    staffs = Registration.objects.filter(User_role='employee')

    salary_structures = SalaryStructure.objects.select_related('employee')

    context = {
        'bok': bok,
        'staffs': staffs,
        'salary_structures': salary_structures,
    }

    return render(
        request,
        'salary_structure_list.html',
        context
    )


# ==========================================
# Add / Update Salary Structure
# ==========================================
def add_salary_structure(request, id):

    bok = Registration.objects.get(id=request.session['logg'])

    employee = get_object_or_404(Registration, id=id)

    salary_structure, created = SalaryStructure.objects.get_or_create(
        employee=employee
    )

    if request.method == 'POST':

        salary_structure.basic_salary = request.POST.get('basic_salary') or 0

        salary_structure.hra = request.POST.get('hra') or 0

        salary_structure.da = request.POST.get('da') or 0

        salary_structure.travel_allowance = request.POST.get(
            'travel_allowance'
        ) or 0

        salary_structure.medical_allowance = request.POST.get(
            'medical_allowance'
        ) or 0

        salary_structure.pf_percentage = request.POST.get(
            'pf_percentage'
        ) or 0

        salary_structure.esi_percentage = request.POST.get(
            'esi_percentage'
        ) or 0

        salary_structure.overtime_rate_per_hour = request.POST.get(
            'overtime_rate_per_hour'
        ) or 0

        salary_structure.save()

        messages.success(
            request,
            'Salary structure updated successfully'
        )

        return redirect('salary_structure_list')

    context = {
        'bok': bok,
        'employee': employee,
        'salary_structure': salary_structure,
    }

    return render(
        request,
        'add_salary_structure.html',
        context
    )


# ==========================================
# Generate Payroll
# ==========================================
def generate_payroll_view(request):

    bok = Registration.objects.get(id=request.session['logg'])

    employees = Registration.objects.filter(User_role='employee')

    if request.method == 'POST':

        month = int(request.POST.get('month'))
        year = int(request.POST.get('year'))

        for employee in employees:

            try:

                # Prevent duplicate payroll
                exists = Payroll.objects.filter(
                    employee=employee,
                    month=month,
                    year=year
                ).exists()

                if exists:
                    continue

                salary = SalaryStructure.objects.get(
                    employee=employee
                )

                total_days = calendar.monthrange(year, month)[1]

                attendance = Attendance.objects.filter(
                    employee=employee,
                    date__month=month,
                    date__year=year
                )

                present_days = attendance.filter(
                    status='Present'
                ).count()

                leave_days = attendance.filter(
                    status='Leave'
                ).count()

                absent_days = total_days - (
                    present_days + leave_days
                )

                gross_salary = salary.gross_salary()

                per_day_salary = (
                    gross_salary / Decimal(total_days)
                )

                leave_deduction = (
                    per_day_salary * Decimal(absent_days)
                )

                extra_hours = ExtraWorkingDay.objects.filter(
                    staff=employee.user,
                    date__month=month,
                    date__year=year
                ).aggregate(
                    total=Sum('hours')
                )['total'] or 0

                overtime_amount = (
                    Decimal(extra_hours)
                    * salary.overtime_rate_per_hour
                )

                pf_amount = (
                    gross_salary
                    * (
                        salary.pf_percentage
                        / Decimal(100)
                    )
                )

                esi_amount = (
                    gross_salary
                    * (
                        salary.esi_percentage
                        / Decimal(100)
                    )
                )

                total_deduction = (
                    leave_deduction
                    + pf_amount
                    + esi_amount
                )

                net_salary = (
                    gross_salary
                    + overtime_amount
                    - total_deduction
                )

                Payroll.objects.create(
                    employee=employee,
                    month=month,
                    year=year,

                    total_working_days=total_days,

                    present_days=present_days,
                    leave_days=leave_days,
                    absent_days=absent_days,

                    overtime_hours=extra_hours,

                    gross_salary=gross_salary,

                    overtime_amount=overtime_amount,

                    leave_deduction=leave_deduction,

                    pf_amount=pf_amount,
                    esi_amount=esi_amount,

                    total_deduction=total_deduction,

                    net_salary=net_salary
                )

            except SalaryStructure.DoesNotExist:
                continue

        messages.success(
            request,
            'Payroll generated successfully'
        )

        return redirect('payroll_list')

    context = {
        'bok': bok,
        'employees': employees,
    }

    return render(
        request,
        'generate_payroll.html',
        context
    )


# ==========================================
# Payroll List
# ==========================================
def payroll_list(request):

    bok = Registration.objects.get(id=request.session['logg'])

    payrolls = Payroll.objects.select_related(
        'employee'
    ).order_by('-year', '-month')

    context = {
        'bok': bok,
        'payrolls': payrolls,
    }

    return render(
        request,
        'payroll_list.html',
        context
    )


# ==========================================
# Payslip List
# ==========================================
def payslip_list(request):

    bok = Registration.objects.get(id=request.session['logg'])

    payrolls = Payroll.objects.select_related(
        'employee'
    ).filter(
        payment_status='Paid'
    ).order_by('-generated_at')

    context = {
        'bok': bok,
        'payrolls': payrolls,
    }

    return render(
        request,
        'payslip_list.html',
        context
    )


# ==========================================
# Payroll Reports
# ==========================================
def payroll_reports(request):

    bok = Registration.objects.get(id=request.session['logg'])

    payrolls = Payroll.objects.all()

    total_salary = payrolls.aggregate(
        total=Sum('net_salary')
    )['total'] or 0

    total_pf = payrolls.aggregate(
        total=Sum('pf_amount')
    )['total'] or 0

    total_esi = payrolls.aggregate(
        total=Sum('esi_amount')
    )['total'] or 0

    total_deduction = payrolls.aggregate(
        total=Sum('total_deduction')
    )['total'] or 0

    context = {
        'bok': bok,
        'payrolls': payrolls,

        'total_salary': total_salary,
        'total_pf': total_pf,
        'total_esi': total_esi,
        'total_deduction': total_deduction,
    }

    return render(
        request,
        'payroll_reports.html',
        context
    )


# ==========================================
# Mark Payroll Paid
# ==========================================
def mark_payroll_paid(request, id):

    payroll = get_object_or_404(
        Payroll,
        id=id
    )

    payroll.payment_status = 'Paid'

    payroll.paid_date = now().date()

    payroll.save()

    messages.success(
        request,
        'Payroll marked as paid'
    )

    return redirect('payroll_list')


def add_salary_structure_page(request):

    bok = Registration.objects.get(
        id=request.session['logg']
    )

    employees = Registration.objects.filter(
        User_role='employee'
    )

    if request.method == 'POST':

        employee_id = request.POST.get('employee')

        employee = Registration.objects.get(
            id=employee_id
        )

        salary_structure, created = SalaryStructure.objects.get_or_create(
            employee=employee
        )

        salary_structure.basic_salary = request.POST.get(
            'basic_salary'
        ) or 0

        salary_structure.hra = request.POST.get(
            'hra'
        ) or 0

        salary_structure.da = request.POST.get(
            'da'
        ) or 0

        salary_structure.travel_allowance = request.POST.get(
            'travel_allowance'
        ) or 0

        salary_structure.medical_allowance = request.POST.get(
            'medical_allowance'
        ) or 0

        salary_structure.pf_percentage = request.POST.get(
            'pf_percentage'
        ) or 0

        salary_structure.esi_percentage = request.POST.get(
            'esi_percentage'
        ) or 0

        salary_structure.overtime_rate_per_hour = request.POST.get(
            'overtime_rate_per_hour'
        ) or 0

        salary_structure.save()

        messages.success(
            request,
            'Salary structure added successfully'
        )

        return redirect('salary_structure_list')

    context = {
        'bok': bok,
        'employees': employees,
    }

    return render(
        request,
        'add_salary_structure_page.html',
        context
    )