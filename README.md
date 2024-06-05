 # Kangaroo Recruitment Management System - RMS
 #### PYTHON | FLASK | PostGreSQL | HTML | CSS | JINJA2 | REDIS | JAVASCRIPT
<br>

### **Home Page of Recruiter**
[![Screenshot-59.png](https://i.postimg.cc/gkbt48SC/Screenshot-59.png)](https://postimg.cc/K4Q58kyf)
<br>
<br>
### **Home Page of Applicant**
[![Screenshot-60.png](https://i.postimg.cc/0QJZ0yp5/Screenshot-60.png)](https://postimg.cc/xJnK0YxB)
<br>
<br>

|      Recruiter      |     Business Partner     |      Applicant      |
|---------------------|--------------------------|---------------------|
| Communicate with business partners, and candidates throughout the recruitment process as well as conducting interviews and assessing candidate qualifications. |  Work with recruiters to provide input on job descriptions, candidate criteria, and interview evaluations. | Apply for job openings within an organization. Submit your resumes, cover letters, and other application materials in response to job postings. |
| Conducts interviews and facilitates the hiring process. | Provides input on candidate evaluations and ensures alignment with team goals. | Participates in interviews and assessments to showcase qualifications. |

<br>

# Getting Started

To run the project locally, follow these steps:

1. Clone the repository: `git clone https://github.com/github_user_name/Kangaroo_RMS.git`
2. Navigate to the project directory: `cd Kangaroo_RMS`
3. Install dependencies: [ <br>`sudo apt install python3`,<br>`pip3 install redis`,<br> `pip3 install Flask`,<br>`sudo apt install redis-server`,<br>`sudo apt install mysql-server`<br> ]
4. Start the development server: `python3 -m backend.backend_api.v1.app`
5. Open your browser and visit: `http://localhost:5000`
<br>

# API Endpoints
### `/applicant/*`  ===  `/recruiter/*`  ===  `/bp/*`

## Main Home Page
- **Endpoint**: `/`
- **Description**: This is the main home page of the recruitment management system.

## Applicant Home Page
- **Endpoint**: `/applicant/homepage`
- **Description**: This is the home page for applicants where they can see an overview of their profile.

## List Published Jobs
- **Endpoint**: `/applicant/jobs`
- **Description**: This endpoint lists all the current published jobs available for applicants to view and apply to.

## Applicant Profile
- **Endpoint**: `/applicant/profile`
- **Description**: This endpoint displays the profile of the applicant, including some personal information.

## Forgot Password
- **Endpoint**: `/applicant/forgot_password`
- **Description**: This endpoint allows applicants to initiate the process to recover their forgotten password.

## Applicant Login
- **Endpoint**: `/applicant/login`
- **Description**: This is the login endpoint for applicants to access their accounts.

## Applicant Logout
- **Endpoint**: `/applicant/logout`
- **Description**: This endpoint allows applicants to log out of their accounts.

## Applicant Signup
- **Endpoint**: `/applicant/signup`
- **Description**: This is the signup endpoint for new applicants to create an account.

## Update Applicant Profile
- **Endpoint**: `/applicant/profile/update`
- **Description**: This endpoint allows applicants to update their profile information.

## Apply to a Job
- **Endpoint**: `/applicant/apply`
- **Description**: This endpoint allows applicants to apply to a job listed on the platform.




<br>
<br>

### Project partners:
> **Nimi Williams**
&nbsp;- Software Architect and Backend-Engineer<br>
> **Joshua Bubune Agbeke**
&nbsp;- Backend-Engineer



