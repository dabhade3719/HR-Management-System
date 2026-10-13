# HR-Management-System

A web-based Human Resource Management System built with **Django**. It covers the everyday work of an HR department: employee records, departments, attendance, leave requests, payroll, recruitment, performance reviews, and in-app notifications, all with role-based access.

---

## Features

| Module | What it does |
| --- | --- |
| **Accounts** | Registration, login/logout, and a separate dashboard for each role (Admin, HR, Manager, Employee). |
| **Employees** | HR/Admin can add, edit, view, search, filter, and delete employee records. Employees can update their own email, phone, address, and photo. |
| **Departments** | Create, edit, search, and delete departments. |
| **Attendance** | Employees check in and check out themselves. HR/Admin can add, edit, and delete records, filter by date or status, and view monthly reports with present/absent/half-day/on-leave totals and total working hours. |
| **Leaves** | Employees apply for Casual, Sick, Paid, or Unpaid leave. HR/Admin approve or reject requests with a comment. |
| **Payroll** | Monthly payroll per employee (basic salary + allowances − deductions = net salary). HR/Admin see all records; employees see only their own. |
| **Recruitment** | HR/Admin post, edit, activate/deactivate, and delete job openings, and track applications through Applied → Shortlisted → Interview → Selected / Rejected. |
| **Performance** | Admin, HR, and Managers write 1–5 star reviews with goals, strengths, areas for improvement, and feedback. Employees can view only their own reviews. |
| **Notifications** | In-app notifications with an unread counter and "mark as read" / "mark all as read". |

### Automatic notifications

- An employee submits a leave request → all HR and Admin users are notified.
- HR/Admin approve or reject a leave request → the employee is notified.
- A payroll record is created → the employee is notified (via a Django signal).
- A new job is posted → all employees are notified.
- Someone applies for a job → all HR and Admin users are notified.

---

## Roles and permissions

| Area | Admin | HR | Manager | Employee |
| --- | :---: | :---: | :---: | :---: |
| Employee management | ✅ | ✅ | ❌ | Own profile only |
| Attendance management and reports | ✅ | ✅ | ❌ | Own check-in/out |
| Leave review (approve/reject) | ✅ | ✅ | ❌ | Apply and view own |
| Payroll list | ✅ | ✅ | ❌ | Own payroll only |
| Recruitment management | ✅ | ✅ | ❌ | Browse and apply for jobs |
| Create performance reviews | ✅ | ✅ | ✅ | ❌ |
| View performance reviews | All | All | All | Own only |

Users who register through the website are given the **Employee** role by default.

---

## Tech stack

- **Backend:** Python, Django 6.1
- **Database:** SQLite (default)
- **Frontend:** Django templates, Bootstrap 5.3 (loaded from a CDN), vanilla JavaScript
- **Other dependencies:** Pillow (for image uploads), asgiref, sqlparse, tzdata

---

## Project structure

```
HR MANAGEMENT/
└── hrms/
    ├── manage.py
    ├── db.sqlite3
    ├── hrms/              # Project settings, root URLs, WSGI/ASGI
    ├── accounts/          # Profile model (roles), auth views, dashboards
    ├── employees/         # Employee model, CRUD, self-service profile
    ├── departments/       # Department model and CRUD
    ├── attendance/        # Attendance model, check-in/out, reports
    ├── leaves/            # Leave requests and review workflow
    ├── payroll/           # Payroll model, signals, views
    ├── requirement/       # Job openings and applications (recruitment)
    ├── performance/       # Performance reviews
    ├── notifications/     # Notification model, context processor, views
    ├── templates/         # HTML templates, one folder per app
    └── static/js/main.js  # Auto-hiding alerts, logout confirmation
```

---

## Getting started

### Prerequisites

- Python 3.12 or newer (this project was developed with Python 3.14)
- `pip`

### Installation

1. **Open a terminal in the project folder** (the one that contains `hrms/`).

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install the dependencies**

   ```bash
   pip install django pillow
   ```

4. **Move into the Django project folder** (where `manage.py` lives)

   ```bash
   cd hrms
   ```

5. **Apply the database migrations**

   ```bash
   python manage.py migrate
   ```

6. **Create an administrator account**

   ```bash
   python manage.py createsuperuser
   ```

7. **Give that account the Admin role** (important, see the note below)

8. **Start the development server**

   ```bash
   python manage.py runserver
   ```

   Open <http://127.0.0.1:8000/> in your browser.

> **Important: setting the Admin role.** The `createsuperuser` command creates a Django superuser but does **not** create the HRMS `Profile` that stores the role. If you log in right away, you will be treated as an Employee.
>
> To fix this, log in at <http://127.0.0.1:8000/admin/> with your superuser account, open **Accounts → Profiles**, add (or edit) a profile for your user, and set its **Role** to `ADMIN`. After that, logging in at `/login/` takes you to the Admin dashboard.

---

## How to use it

### Setting up users and employees

1. A person registers at `/register/` (they become an **Employee** user).
2. An Admin changes their role to `HR` or `MANAGER` where needed (**Django admin → Accounts → Profiles**).
3. An Admin or HR user goes to **Employees → Add** and creates the employee record by entering the person's **existing username** plus their details (employee ID, department, designation, joining date, salary, and so on). This links the user account to the employee record.

Every employee-specific feature (attendance check-in, performance reviews, and so on) requires this linked employee record.

### Creating payroll

There is no payroll form in the main interface. Payroll records are created in the **Django admin** (`/admin/` → **Payroll**). Net salary is calculated automatically on save, and the employee is notified. HR/Admin view all records at `/payroll/`, and employees view their own at `/payroll/my/`.

---

## Main URLs

| URL | Purpose |
| --- | --- |
| `/` | Home page |
| `/register/`, `/login/`, `/logout/` | Authentication |
| `/dashboard/` | Redirects to the dashboard for your role |
| `/employees/` | Employee list (HR/Admin) |
| `/profile/` | My profile (Employee) |
| `/departments/` | Departments |
| `/attendance/`, `/attendance/report/` | Attendance list and report (HR/Admin) |
| `/my-attendance/` | Check in / check out (Employee) |
| `/leaves/apply/`, `/leaves/my/` | Apply for leave, view my leaves |
| `/leaves/manage/` | Review leave requests (HR/Admin) |
| `/payroll/`, `/payroll/my/` | Payroll (HR/Admin), my payroll (Employee) |
| `/requirement/` | Recruitment dashboard (HR/Admin) |
| `/requirement/jobs/` | Browse open jobs |
| `/requirement/applications/` | Manage applications (HR/Admin) |
| `/performance/` | Performance reviews |
| `/notifications/` | Notifications |
| `/admin/` | Django admin site |

---

## Data models at a glance

- **Profile**: one-to-one with `User`; stores `role` (Admin / HR / Manager / Employee), phone, and photo.
- **Employee**: one-to-one with `User`; ID, name, contact details, department, designation, joining date, salary, employment status (Active / Inactive / On Leave / Resigned).
- **Department**: name, description, active flag.
- **Attendance**: employee, date, check-in/out, status, remarks; one record per employee per day.
- **LeaveRequest**: employee, type, dates, reason, status, reviewer, review comment.
- **Payroll**: employee, month, year, basic salary, allowances, deductions, net salary, paid flag; one record per employee per month.
- **JobOpening** and **JobApplication**: recruitment data.
- **PerformanceReview**: employee, reviewer, review period, rating (1–5), written feedback.
- **Notification**: user, title, message, type, read flag.

---

## Known limitations and suggested improvements

These are things worth fixing before using the project beyond local development:

- **Department pages have no access control.** The department views do not check login or role, so anyone who can reach the URL can view, add, edit, or delete departments. Add `@login_required` and an Admin/HR role check.
- **Uploaded photos are not served.** `MEDIA_URL` and `MEDIA_ROOT` are not configured in `settings.py`, and no media URL route is defined, so uploaded profile photos will not display. Configure both and add `static()` media routes for development.
- **Manager dashboard is a placeholder.** It currently shows only a logout link. Managers can reach `/performance/` directly by URL.
- **Production settings.** `SECRET_KEY` is hard-coded, `DEBUG = True`, and `ALLOWED_HOSTS` is empty. Move secrets to environment variables and turn `DEBUG` off before deploying.
- **Email.** No real email backend is configured, so no emails are sent.
- **Repository hygiene.** Do not commit `venv/` or `db.sqlite3`. Add a `.gitignore` and a `requirements.txt` (for example via `pip freeze > requirements.txt`).
- **Tests.** The `tests.py` files are empty; adding tests for permissions and the payroll calculation would be a good start.

---

## License

No license has been specified for this project. Add one (for example MIT) if you plan to share it.
