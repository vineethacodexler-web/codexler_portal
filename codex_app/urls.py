from django.urls import path
from . import views
from django.contrib import admin
from .views import  admin_home
from django.urls import path
from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
from .views import project_list
from django.urls import path
from .views import  add_project, edit_project, delete_project

urlpatterns = [
    path('',views.home,name = 'home'),
    path('home',views.home,name = 'home'),
    path('adminn',views.admin_rg,name = 'adminn'),
    path('delete_admin', views.delete_admin, name='delete_admin'),
    path('edit_admin', views.edit_admin, name='edit_admin'),
    path('admin_rg',views.admin_rg, name='admin_rg'),
    path('bnb', views.bnb, name='bnb'),
    path('del_admin/<id>', views.del_admin, name='del_admin'),
      path('del_employee/<id>', views.del_employee, name='del_employee'),
    path('edit_admin',views.edit_admin, name='edit_admin'),
    path('logged_out', views.logged_out, name='logged_out'),
    path('login/',views.login,name = 'login'),
    path('logout', views.logout, name='logout'),
    path('admin_home',views.admin_home, name='admin_home'),
    path('adminn_details', views.adminn_details, name='adminn_details'),
    path('register_employee', views.register_employee, name='register_employee'),
        path('employeess', views.employeess, name='employeess'),
        path('employee_home', views.employee_home, name='employee_home'),
        path('update_employee', views.update_employee, name='update_employee'),
        path('update_employeee', views.update_employeee, name='update_employeee'),
path('view_staffs', views.view_staffs, name='view_staffs'),
path('update_employeee/<int:employee_id>/', views.update_employeee, name='update_employeee'),

    path('add_project', views.add_project, name='add_project'),
    path('create_timesheet_staff', views.create_timesheet_staff, name='create_timesheet_staff'),
        path('create_timesheet_admin', views.create_timesheet_admin, name='create_timesheet_admin'),
    path('mark_attendance', views.mark_attendance, name='mark_attendance'),
path('mark_attendance_staff', views.mark_attendance_staff, name='mark_attendance_staff'),
path('add_timesheet_admin', views.add_timesheet_admin, name='add_timesheet_admin'),
path('add_timesheet_staff', views.add_timesheet_staff, name='add_timesheet_staff'),
path('view_timesheet_admin/<int:timesheet_id>', views.view_timesheet_admin, name='view_timesheet_admin'),
    path('view_timesheets_staff', views.view_timesheets_staff, name='view_timesheets_staff'),
    path('view_timesheets_admin', views.view_timesheets_admin, name='view_timesheets_admin'),

path('update_timesheet/<int:timesheet_id>/', views.update_timesheet, name='update_timesheet'),
   path('delete_timesheet_admin/<int:timesheet_id>/', views.delete_timesheet_admin, name='delete_timesheet_admin'),
    path('delete_timesheet_staff/<int:timesheet_id>/', views.delete_timesheet_staff, name='delete_timesheet_staff'),
    path('delete_timesheet_staff_all/<int:timesheet_id>/', views.delete_timesheet_staff_all, name='delete_timesheet_staff_all'),


  path('update_leave_staff/<int:leave_id>', views.update_leave_staff, name='update_leave_staff'),
     path('apply_leave_staff', views.apply_leave_staff, name='apply_leave_staff'),
    path('view_leaves_staff', views.view_leaves_staff, name='view_leaves_staff'),
    path('update_leave_admin/<int:leave_id>', views.update_leave_admin, name='update_leave_admin'),
    path('delete_leave_staff/<int:leave_id>', views.delete_leave_staff, name='delete_leave_staff'),
 path('delete_leave_admin/<int:leave_id>', views.delete_leave_admin, name='delete_leave_admin'),
    path('add_project', views.add_project, name='add_project'),
  path('project/edit/<int:project_id>/', views.edit_project, name='edit_project'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),


  path('api/projects/', project_list, name='project-list'),
    

  path('all_view_timesheet_admin', views.all_view_timesheet_admin, name='all_view_timesheet_admin'),

  path('all_view_timesheet', views.all_view_timesheet, name='all_view_timesheet'),

     path('apply_leave_admin', views.apply_leave_admin, name='apply_leave_admin'),
    path('view_leaves_admin', views.view_leaves_admin, name='view_leaves_admin'),

    path('view_timesheets_staff', views.view_timesheets_staff, name='view_timesheets_staff'),

    # URL for updating an existing timesheet (the 'timesheet_id' parameter is required)
    path('update_timesheet_admin/<int:timesheet_id>/', views.update_timesheet_admin, name='update_timesheet_admin'),




  path('view_timesheet/<int:timesheet_id>', views.view_timesheet, name='view_timesheet'),



 path('delete_leave_admin_all/<int:leave_id>', views.delete_leave_admin_all, name='delete_leave_admin_all'),



    path('view_staff_detail/<int:id>/', views.view_staff_detail, name='view_staff_detail'),

          path('view_staff_details/<id>', views.view_staff_details, name='view_staff_details'),





              path('worked_staffs/<int:project_id>/', views.worked_staffs, name='worked_staffs'),

path('view_all_timesheets', views.view_all_timesheets, name='view_all_timesheets'),

path('view_all_timesheets_admin', views.view_all_timesheets_admin, name='view_all_timesheets_admin'),
path('view_leaves_admin_all', views.view_leaves_admin_all, name='view_leaves_admin_all'),


path('view_leaves_admin', views.view_leaves_admin, name='view_leaves_admin'),

path('view_all_timesheets_admins', views.view_all_timesheets_admins, name='view_all_timesheets_admins'),

path('view_attendance', views.view_attendance, name='view_attendance'),
    path('delete-leave/<int:leave_id>/', views.delete_leave_admin_all, name='delete_leave_admin_all'),
   path('submit_additional_day', views.submit_additional_day, name='submit_additional_day'),
      path('submit_additional_day_admin', views.submit_additional_day_admin, name='submit_additional_day_admin'),

 path('view_additional_days', views.view_additional_days, name='view_additional_days'),
    path('update_additional_day/<int:day_id>/', views.update_additional_day, name='update_additional_day'),
    path('delete_additional_day/<int:day_id>/', views.delete_additional_day, name='delete_additional_day'),

     path('view_additional_days_a', views.view_additional_days_a, name='view_additional_days_a'),
 path('view_additional_days_admin', views.view_additional_days_admin, name='view_additional_days_admin'),

     path('update_additional_day_a/<int:day_id>/', views.update_additional_day_a, name='update_additional_day_a'),
    path('delete_additional_day_a/<int:day_id>/', views.delete_additional_day_a, name='delete_additional_day_a'),




path('services', views.services, name='services'),


path('contactus', views.contactus, name='contactus'),
path('contact/', views.contact_view, name='contact'),


path('careers', views.careers, name='careers'),

path('about', views.about, name='about'),


path('services/web-development/', views.web_development, name='web_development'),
path('services/mobile-apps/', views.mobile_apps, name='mobile_apps'),
path('services/digital-marketing/', views.digital_marketing, name='digital_marketing'),

path('services/custom-software/', views.custom_software, name='custom_software'),
path('services/ai-solutions/', views.ai_solutions, name='ai_solutions'),
path('services/cloud-solutions/', views.cloud_solutions, name='cloud_solutions'),
path('expense_list/', views.expense_list, name='expense_list'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('edit_expense/<int:id>/', views.edit_expense, name='edit_expense'),
    path('delete_expense/<int:id>/', views.delete_expense, name='delete_expense'),

path('category/', views.category_list, name='category_list'),
path('category/add/', views.add_category, name='add_category'),
path('category/edit/<int:id>/', views.edit_category, name='edit_category'),
path('category/delete/<int:id>/', views.delete_category, name='delete_category'),
path('export-excel/', views.export_excel, name='export_excel'),
    path("f_dashboard/",views.f_dashboard,name="f_dashboard"),
    path('client_payments/', views.client_payments, name='client_payments'),
    path('other_income/', views.other_income, name='other_income'),
    path('recurring_income/', views.recurring_income, name='recurring_income'),
path('clients/', views.client_list, name='client_list'),
path('delete_client/<int:id>/', views.delete_client, name='delete_client'),
path('projects/', views.projects, name='projects'),
path('project_income', views.project_income, name='project_income'),
path('project_expenses', views.project_expenses, name='project_expenses'),
path('project_profit', views.project_profit, name='project_profit'),
path('payment_history', views.payment_history, name='payment_history'),
path('pending_payments', views.pending_payments, name='pending_payments'),
path('transactions', views.transactions, name='transactions'),
path('profit_loss', views.profit_loss, name='profit_loss'),
path('cash_flow', views.cash_flow, name='cash_flow'),
path('monthly_report', views.monthly_report, name='monthly_report'),
    path("register_accounts/",views.register_accounts, name="register_accounts"),
path('salary-structure-list/', views.salary_structure_list, name='salary_structure_list'),

path('generate-payroll/', views.generate_payroll_view, name='generate_payroll'),

path('payroll-list/', views.payroll_list, name='payroll_list'),

path('payslip-list/', views.payslip_list, name='payslip_list'),

path('payroll-reports/', views.payroll_reports, name='payroll_reports'),
path('add-salary-structure-page/',views.add_salary_structure_page,name='add_salary_structure_page'),
path('add_salary_structure/<int:id>/',views.add_salary_structure,name='add_salary_structure'),
path('mark-payroll-paid/<int:id>/',views.mark_payroll_paid,name='mark_payroll_paid'),
path('view-payslip/<int:id>/',views.view_payslip,name='view_payslip'),
path('download-payslip-pdf/<int:id>/',views.download_payslip_pdf,name='download_payslip_pdf'),
path('lead-list/', views.lead_list, name='lead_list'),

path('add-lead/', views.add_lead, name='add_lead'),
path(
    'followup-list/',
    views.followup_list,
    name='followup_list'
),

path(
    'add-followup/',
    views.add_followup,
    name='add_followup'
),

path(
    'communication-list/',
    views.communication_list,
    name='communication_list'
),

path(
    'add-communication/',
    views.add_communication,
    name='add_communication'
),

path(
    'support-ticket-list/',
    views.support_ticket_list,
    name='support_ticket_list'
),

path(
    'add-support-ticket/',
    views.add_support_ticket,
    name='add_support_ticket'
),
path(
    'crm-dashboard/',
    views.crm_dashboard,
    name='crm_dashboard'
),
]





