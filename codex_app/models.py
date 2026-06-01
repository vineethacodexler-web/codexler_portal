from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Designation(models.Model):

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='designations'
    )

    title = models.CharField(max_length=100)

    description = models.TextField(
        null=True,
        blank=True
    )

    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title



# =========================
# Registration Model
# =========================
class Registration(models.Model):
    Emp_Id = models.CharField(max_length=200, null=True, blank=True)
    First_name = models.CharField(max_length=200, null=True, blank=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    designation = models.ForeignKey(
        Designation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    Email = models.EmailField(max_length=200, null=True, blank=True)
    Password = models.CharField(max_length=200, null=True, blank=True)
    Mobile_Number = models.CharField(max_length=200, null=True, blank=True)
    Registration_date = models.DateField(null=True, blank=True)
    Image = models.ImageField(upload_to='images/', null=True, blank=True)
    Gender = models.CharField(max_length=200, null=True, blank=True)
    Address = models.CharField(max_length=1000, null=True, blank=True)
    Location = models.CharField(max_length=1000, null=True, blank=True)
    User_role = models.CharField(max_length=200, null=True, blank=True)

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.First_name or "Employee"




class EmployeeDocument(models.Model):

    DOCUMENT_TYPES = (
        ('Aadhaar', 'Aadhaar'),
        ('PAN', 'PAN'),
        ('Resume', 'Resume'),
        ('Offer Letter', 'Offer Letter'),
        ('Experience Certificate', 'Experience Certificate'),
        ('Educational Certificate', 'Educational Certificate'),
        ('Other', 'Other'),
    )

    employee = models.ForeignKey(
        Registration,
        on_delete=models.CASCADE,
        related_name='documents'
    )

    document_type = models.CharField(
        max_length=100,
        choices=DOCUMENT_TYPES
    )

    document_name = models.CharField(
        max_length=255
    )

    document_file = models.FileField(
        upload_to='employee_documents/'
    )

    remarks = models.TextField(
        null=True,
        blank=True
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.employee.First_name} - {self.document_name}"



class EmployeeExperience(models.Model):

    employee = models.ForeignKey(
        Registration,
        on_delete=models.CASCADE,
        related_name='experiences'
    )

    company_name = models.CharField(
        max_length=200
    )

    designation = models.CharField(
        max_length=200
    )

    start_date = models.DateField()

    end_date = models.DateField(
        null=True,
        blank=True
    )

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    responsibilities = models.TextField(
        null=True,
        blank=True
    )

    experience_certificate = models.FileField(
        upload_to='experience_certificates/',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.employee.First_name} - {self.company_name}"




class Appraisal(models.Model):

    employee = models.ForeignKey(
        Registration,
        on_delete=models.CASCADE,
        related_name='appraisals'
    )

    review_date = models.DateField()

    review_period = models.CharField(
        max_length=100,
        help_text="Example: Jan 2026 - Jun 2026"
    )

    rating = models.IntegerField(
        default=1
    )

    current_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    proposed_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    salary_hike = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    promotion = models.BooleanField(
        default=False
    )

    remarks = models.TextField(
        null=True,
        blank=True
    )

    reviewed_by = models.ForeignKey(
        Registration,
        on_delete=models.SET_NULL,
        null=True,
        related_name='reviews_given'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.employee.First_name} - {self.review_date}"

# =========================
# Attendance
# =========================

class Attendance(models.Model):

    employee = models.ForeignKey(
        Registration,
        on_delete=models.CASCADE,
        related_name="attendance_records",
        null=True,
        blank=True
    )

    date = models.DateField(default=now)

    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=50,
        choices=[
            ("Present", "Present"),
            ("Absent", "Absent"),
            ("Leave", "Leave")
        ],
        default="Present"
    )

    total_working_hours = models.FloatField(default=0.0)

    webcam_image_in = models.ImageField(
        upload_to='attendance_images/',
        null=True,
        blank=True
    )

    webcam_image_out = models.ImageField(
        upload_to='attendance_images/',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.employee} - {self.date}"

# =========================
# Leave Balance
# =========================
class LeaveBalance(models.Model):
    staff = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    casual_leaves = models.IntegerField(default=12, null=True, blank=True)
    sick_leaves = models.IntegerField(default=6, null=True, blank=True)
    compensatory_leaves = models.IntegerField(default=0, null=True, blank=True)
    additional_working_days = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.staff}"


# =========================
# Leave Application
# =========================
class LeaveApplication(models.Model):

    LEAVE_TYPE_CHOICES = [
        ('Casual', 'Casual'),
        ('Sick', 'Sick'),
        ('Compensatory', 'Compensatory')
    ]

    staff = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    leave_type = models.CharField(
        max_length=20,
        choices=LEAVE_TYPE_CHOICES,
        null=True,
        blank=True
    )

    date_from = models.DateTimeField(null=True, blank=True)
    date_to = models.DateTimeField(null=True, blank=True)

    total_days = models.IntegerField(null=True, blank=True)

    reason = models.TextField(null=True, blank=True)

    document = models.FileField(
        upload_to='leave_documents/',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.staff} - {self.leave_type}"


# =========================
# Additional Working Day
# =========================
class AdditionalWorkingDay(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    submitted_at = models.DateField(auto_now_add=True)


# =========================
# Extra Working Day
# =========================
class ExtraWorkingDay(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    hours = models.FloatField(default=8.0, null=True, blank=True)

    def __str__(self):
        return f"{self.staff} - {self.date}"


# =========================
# Project
# =========================
class CreateProject(models.Model):
    employee = models.ForeignKey(
        Registration,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    project_name = models.CharField(max_length=255, null=True, blank=True)
    project_no = models.CharField(max_length=100, unique=True, null=True, blank=True)
    remarks = models.CharField(max_length=100, null=True, blank=True)
    week_no = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.project_name or "Project"


# =========================
# Timesheet
# =========================
class Create_Timesheet(models.Model):

    project = models.ForeignKey(
        CreateProject,
        on_delete=models.CASCADE,
        related_name="timesheets",
        null=True,
        blank=True
    )

    staff_list = models.ForeignKey(
        Registration,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    staff_id = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    total_hours_taken = models.IntegerField(default=0, null=True, blank=True)


# =========================
# Timesheet Line
# =========================
class Create_Timesheet_Line(models.Model):

    timesheet = models.ForeignKey(
        Create_Timesheet,
        on_delete=models.CASCADE,
        related_name="timesheet_lines",
        null=True,
        blank=True
    )

    staff_list = models.ForeignKey(
        Registration,
        on_delete=models.CASCADE,
        related_name="timesheet_lines",
        null=True,
        blank=True
    )

    project_name = models.CharField(max_length=200, null=True, blank=True)
    project_no = models.CharField(max_length=200, null=True, blank=True)
    remarks = models.CharField(max_length=200, null=True, blank=True)

    date = models.DateField(null=True, blank=True)
    total_hours_taken = models.IntegerField(default=0, null=True, blank=True)

    duration_hours = models.IntegerField(default=0, null=True, blank=True)
    duration_minutes = models.IntegerField(default=0, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.timesheet and not self.staff_list:
            self.staff_list = self.timesheet.staff_list
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.project_name}"

    def get_week_dates(self):
        start = self.date
        return {
            'mon': (start + timedelta(days=0)).strftime('%d-%b'),
            'tue': (start + timedelta(days=1)).strftime('%d-%b'),
            'wed': (start + timedelta(days=2)).strftime('%d-%b'),
            'thu': (start + timedelta(days=3)).strftime('%d-%b'),
            'fri': (start + timedelta(days=4)).strftime('%d-%b'),
            'sat': (start + timedelta(days=5)).strftime('%d-%b'),
            'sun': (start + timedelta(days=6)).strftime('%d-%b'),
        }



class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Expense(models.Model):
    category = models.ForeignKey(ExpenseCategory, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True)
    receipt = models.FileField(upload_to='expenses/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.amount}"


class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.name


# Project Model
class Project(models.Model):
    name = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name




# Income Model (MAIN)
class Income(models.Model):
    INCOME_TYPE = (
        ('client', 'Client Payment'),
        ('other', 'Other Income'),
        ('recurring', 'Recurring Income'),
    )

    type = models.CharField(max_length=20, choices=INCOME_TYPE)

    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)

    source = models.CharField(max_length=100, blank=True, null=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    payment_mode = models.CharField(max_length=50, blank=True, null=True)

    # Recurring fields
    frequency = models.CharField(max_length=20, blank=True, null=True)

    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.type} - {self.amount}"



class ProjectIncome(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.project.name} - {self.amount}"


# -----------------------------
# PROJECT EXPENSE
# -----------------------------
class ProjectExpense(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    expense_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.project.name} - {self.amount}"


class SalaryStructure(models.Model):

    employee = models.OneToOneField(
        Registration,
        on_delete=models.CASCADE,
        related_name='salary_structure'
    )

    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    hra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    da = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    travel_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    medical_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    pf_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=12)

    esi_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.75)

    overtime_rate_per_hour = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=100
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def gross_salary(self):
        return (
            self.basic_salary +
            self.hra +
            self.da +
            self.travel_allowance +
            self.medical_allowance
        )

    def __str__(self):
        return f"{self.employee.First_name}"

class Payroll(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
    )

    employee = models.ForeignKey(
        Registration,
        on_delete=models.CASCADE
    )

    month = models.IntegerField()
    year = models.IntegerField()

    total_working_days = models.IntegerField(default=0)

    present_days = models.IntegerField(default=0)

    leave_days = models.IntegerField(default=0)

    absent_days = models.IntegerField(default=0)

    overtime_hours = models.FloatField(default=0)

    gross_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    overtime_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    leave_deduction = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    pf_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    esi_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    bonus = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    incentive = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    total_deduction = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    net_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    payment_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    paid_date = models.DateField(null=True, blank=True)

    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employee', 'month', 'year')

    def __str__(self):
        return f"{self.employee.First_name} - {self.month}/{self.year}"


class Lead(models.Model):

    STATUS_CHOICES = (
        ('New', 'New'),
        ('Contacted', 'Contacted'),
        ('Qualified', 'Qualified'),
        ('Converted', 'Converted'),
        ('Lost', 'Lost'),
    )

    name = models.CharField(max_length=200)

    email = models.EmailField(blank=True, null=True)

    phone = models.CharField(max_length=20, blank=True, null=True)

    company = models.CharField(max_length=200, blank=True, null=True)

    source = models.CharField(max_length=100, blank=True, null=True)

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='New'
    )

    assigned_to = models.ForeignKey(
        Registration,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)


class FollowUp(models.Model):

    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name='followups'
    )

    followup_date = models.DateTimeField()

    remarks = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=50,
        choices=(
            ('Pending', 'Pending'),
            ('Completed', 'Completed'),
            ('Missed', 'Missed'),
        ),
        default='Pending'
    )

    created_by = models.ForeignKey(
        Registration,
        on_delete=models.SET_NULL,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)


class CommunicationHistory(models.Model):

    TYPE_CHOICES = (
        ('Call', 'Call'),
        ('Email', 'Email'),
        ('Meeting', 'Meeting'),
        ('WhatsApp', 'WhatsApp'),
    )

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE
    )

    communication_type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES
    )

    subject = models.CharField(max_length=255)

    message = models.TextField()

    communication_date = models.DateTimeField(auto_now_add=True)

    handled_by = models.ForeignKey(
        Registration,
        on_delete=models.SET_NULL,
        null=True
    )


class SupportTicket(models.Model):

    PRIORITY_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    )

    STATUS_CHOICES = (
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    )

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    subject = models.CharField(max_length=255)

    description = models.TextField()

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='Medium'
    )

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='Open'
    )

    assigned_to = models.ForeignKey(
        Registration,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    attachment = models.FileField(
        upload_to='tickets/',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)


class TicketResolution(models.Model):

    ticket = models.ForeignKey(
        SupportTicket,
        on_delete=models.CASCADE,
        related_name='resolutions'
    )

    status = models.CharField(
        max_length=50
    )

    remarks = models.TextField()

    updated_by = models.ForeignKey(
        Registration,
        on_delete=models.SET_NULL,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.ticket.subject} - {self.status}"

class ProjectMember(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='members'
    )

    employee = models.ForeignKey(
        Registration,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    assigned_date = models.DateField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            'project',
            'employee'
        )

    def __str__(self):
        return f"{self.project.name} - {self.employee.First_name}"


class Task(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('On Hold', 'On Hold'),
    )

    PRIORITY_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )

    assigned_to = models.ForeignKey(
        Registration,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=255
    )

    description = models.TextField(
        null=True,
        blank=True
    )

    start_date = models.DateField()

    due_date = models.DateField()

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='Medium'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    progress = models.IntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title



class ProjectMilestone(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='milestones'
    )

    title = models.CharField(
        max_length=255
    )

    description = models.TextField(
        null=True,
        blank=True
    )

    start_date = models.DateField()

    target_date = models.DateField()

    completed_date = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    progress = models.IntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title



class Bug(models.Model):

    PRIORITY_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    )

    STATUS_CHOICES = (
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Testing', 'Testing'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )

    task = models.ForeignKey(
        Task,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    reported_by = models.ForeignKey(
        Registration,
        on_delete=models.SET_NULL,
        null=True,
        related_name='bugs_reported'
    )

    assigned_to = models.ForeignKey(
        Registration,
        on_delete=models.SET_NULL,
        null=True,
        related_name='bugs_assigned'
    )

    title = models.CharField(
        max_length=255
    )

    description = models.TextField()

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='Medium'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Open'
    )

    attachment = models.FileField(
        upload_to='bug_files/',
        null=True,
        blank=True
    )

    resolution_notes = models.TextField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title


class ProjectFile(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='files'
    )

    uploaded_by = models.ForeignKey(
        Registration,
        on_delete=models.SET_NULL,
        null=True
    )

    title = models.CharField(
        max_length=255
    )

    description = models.TextField(
        null=True,
        blank=True
    )

    file = models.FileField(
        upload_to='project_files/'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title