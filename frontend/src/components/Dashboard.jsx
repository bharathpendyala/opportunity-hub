import {useEffect} from "react";
import {useAuth} from "../contexts/Contexts";
import {useState} from "react";
import {useNavigate} from "react-router-dom";
import CandidateDashboard from "./CandidateDashboard";

import CandidateMenu from "./JobseekerMenu";
import Breadcrumbs from "./Breadcrumbs";
import CompanyDashboard from "./CompanyDashboard";
export default function Dashboard() {
    const {user, isAuthenticated, fetchUserData} = useAuth();
    const navigate = useNavigate();

    // if (!isAuthenticated) {
    //     return <div>Not authenticated...</div>;
    // }
    // console.log(user);
    // if (!user) {
    //     // Render loading state or redirect to login page
    //     console.log("loading");
    //     return <div>Loading...</div>;
    // }

    useEffect(() => {
        // if (!isAuthenticated) {
        //     navigate("/login");
        // } else {
        //     fetchUserData();
        // }
    }, [isAuthenticated, fetchUserData, navigate]);

    if (!isAuthenticated) {
        return <div>Not authenticated...</div>;
    }

    if (!user) {
        return <div>Loading...</div>;
    }

    return <div>{user.user_type === "company" ? <CompanyDashboard /> : <CandidateDashboard />}</div>;

    //     <>
    //         {" "}
    //         <Breadcrumbs
    //             pageTitle="Profile Dashboard"
    //             pageInfo="Editing and updating a profile profile allows you to keep information current and accurate,
    //             while also allowing companies to find you."
    //         />
    //         <div className="bookmarked section">
    //             <div className="container">
    //                 {/* {% if messages %}
    //         <div className="alert alert-danger" role="alert">

    //             <ul className="messages">
    //                 {% for message in messages %}
    //                 <li>{{ message }}</li>
    //                 {% endfor %}
    //             </ul>
    //         </div>
    //         {% endif %} */}
    //                 <div className="alerts-inner">
    //                     <div className="row">
    //                         <CandidateMenu />

    //                         <div className="col-lg-8 col-12">
    //                             <div className="cat-head job-category">
    //                                 <div className="row">
    //                                     <div className="col-md-4 col-12">
    //                                         <a href="{% url 'jobs-apply' %}" className="single-cat wow fadeInUp">
    //                                             <div className="icon">{/* <i>{{all_jobs_accepted}}</i> */}</div>
    //                                             <h3>
    //                                                 Approved <br /> applications
    //                                             </h3>
    //                                         </a>
    //                                     </div>
    //                                     <div className="col-md-4 col-12">
    //                                         <a href="{% url 'jobs-apply' %}" className="single-cat wow fadeInUp">
    //                                             <div className="icon">{/* <i>{{all_jobs_pending}}</i> */}</div>
    //                                             <h3>
    //                                                 Pending
    //                                                 <br /> applications
    //                                             </h3>
    //                                         </a>
    //                                     </div>

    //                                     <div className="col-md-4 col-12">
    //                                         <a href="{% url 'jobs-apply' %}" className="single-cat wow fadeInUp">
    //                                             <div className="icon">{/* <i>{{all_jobs_rejected}}</i> */}</div>
    //                                             <h3>
    //                                                 Rejected
    //                                                 <br /> applications
    //                                             </h3>
    //                                         </a>
    //                                     </div>
    //                                 </div>

    //                                 <div className="resume ">
    //                                     <div className="container">
    //                                         <div className="resume-inner">
    //                                             <div className="row">
    //                                                 <div className="col-lg-12 col-12">
    //                                                     <div className="inner-content">
    //                                                         <div className="personal-top-content">
    //                                                             <div className="row">
    //                                                                 <div className="col-lg-5 col-md-5 col-12">
    //                                                                     <div className="name-head">
    //                                                                         {user.user.profile_picture && (
    //                                                                             <a className="mb-2" href="#">
    //                                                                                 <img className="circle-54" src={`https://res.cloudinary.com/drjgddl0y/${user.user.profile_picture}`} alt="" />
    //                                                                             </a>
    //                                                                         )}
    //                                                                         {/* {% if user.candidate.profile_picture %}
    //                                         <a className="mb-2" href="#"><img className="circle-54"
    //                                                 src="{{ user.candidate.profile_picture.url}}" alt=""></a>
    //                                         {% endif %}
    //                                         <h4><a className="name" href="#">{{ user.candidate.first_name}} {{ user.candidate.last_name }}</a></h4>
    //                                         <p><a className="deg" href="#">{{ user.candidate.occupation}}</a></p>
    //                                         <ul className="social">
    //                                             {% if user.candidate.facebook %}
    //                                             <li><a target="_blank" href="{{ user.candidate.facebook }}"><i className="lni lni-facebook-original"></i></a></li>
    //                                             {% endif %}

    //                                             {% if user.candidate.linkedin %}
    //                                             <li><a target="_blank" href="{{ user.candidate.linkedin }}"><i className="lni lni-linkedin-original"></i></a></li>
    //                                             {% endif %}

    //                                             {% if user.candidate.github %}
    //                                             <li><a target="_blank" href="{{ user.candidate.github }}"><i className="lni lni-github"></i></a></li>
    //                                             {% endif %}
    //                                         </ul> */}
    //                                                                     </div>
    //                                                                 </div>
    //                                                                 <div className="col-lg-7 col-md-7 col-12">
    //                                                                     <div className="content-right">
    //                                                                         <h5 className="title-main">Profile Information</h5>

    //                                                                         <div className="single-list">
    //                                                                             <h5 className="title">Location</h5>
    //                                                                             <p>{user.user.city}</p>
    //                                                                         </div>

    //                                                                         <div className="single-list">
    //                                                                             <h5 className="title">E-mail</h5>
    //                                                                             <p> {user.email} </p>
    //                                                                         </div>

    //                                                                         <div className="single-list">
    //                                                                             <h5 className="title">Phone</h5>
    //                                                                             <p>{user.user.phone_number}</p>
    //                                                                         </div>

    //                                                                         <div className="single-list">
    //                                                                             <h5 className="title">Website</h5>
    //                                                                             <p>
    //                                                                                 <a target="_blank" href={user.user.website}>
    //                                                                                     Link
    //                                                                                 </a>
    //                                                                             </p>
    //                                                                         </div>
    //                                                                     </div>
    //                                                                 </div>
    //                                                             </div>
    //                                                         </div>

    //                                                         <div className="single-section">
    //                                                             <h4>About</h4>
    //                                                             <p className="font-size-4 mb-8">{user.user.about}</p>
    //                                                         </div>

    //                                                         <div className="single-section skill">
    //                                                             <h4>Skills</h4>
    //                                                             <ul className="list-unstyled d-flex align-items-center flex-wrap">
    //                                                                 {/* {%  for skill in request.user.candidate.skills.all %}
    //                                   <li>
    //                                     <a href="#">{{ skill}}</a>
    //                                 </li>
    //                                 {% endfor %} */}
    //                                                             </ul>
    //                                                         </div>

    //                                                         <div className="single-section exprerience">
    //                                                             {/* <a style="float: right" className="education-link" href="{% url 'add-work-experience' user.candidate.pk %}">
    //                                                             Add Work Experience{" "}
    //                                                         </a> */}
    //                                                             <h4>Work Experience</h4>
    //                                                             {/*
    //                             {% for experience in user.candidate.experience.all %}

    //                             <div className="single-exp mb-30">
    //                                 <div className="d-flex align-items-center pr-11 mb-9 flex-wrap flex-sm-nowrap">
    //                                     <div className="image">
    //                                         {% if experience.image %}
    //                                             <img src="{{ experience.image}}" alt="#" width="80" height="80">
    //                                         {% else %}
    //                                         <img  width="80" height="80" src="{% static '/images/resume/work.jpg' %}" alt="#">
    //                                         {% endif %}
    //                                     </div>
    //                                     <div className="w-100 mt-n2">
    //                                         <h3 className="mb-0">
    //                                             <a href="#"> {{ experience.company }} </a>
    //                                         </h3>

    //                                         <p>{{ experience.description|safe }}</p>
    //                                         <div className="d-flex align-items-center justify-content-md-between flex-wrap">
    //                                             <p>{{ experience.start_date}} - {{ experience.end_date}}</p>
    //                                             <div>
    //                                             <a  href="{% url 'edit-work-experience' experience.pk %}" className="education-edit font-size-3">Edit</a>
    //                                              <a  style="color: red; margin-left: 20px" href="{% url 'delete work experience' experience.pk %}" className="education-edit font-size-3">Delete</a>
    //                                             </div>
    //                                             </div>
    //                                     </div>
    //                                 </div>
    //                             </div>
    //                             {% endfor %} */}
    //                                                         </div>

    //                                                         <div className="single-section education">
    //                                                             {/* <a style="float: right" className="education-link" href="{% url 'add-education' user.candidate.pk %}">
    //                                                             Add Education
    //                                                         </a> */}
    //                                                             <h4>Education</h4>

    //                                                             {/* {%  for education in request.user.candidate.educations.all %}
    //                             <div className="single-edu mb-30">
    //                                 <div className="d-flex align-items-center pr-11 mb-9 flex-wrap flex-sm-nowrap">
    //                                     <div className="image" >
    //                                         {% if education.image %}
    //                                         <img src="{{ education.image}}" alt="#" width="80" height="80">
    //                                         {% else %}
    //                                         <img src="{% static 'images/resume/education.jpg' %}" alt="#" width="80" height="80">
    //                                         {% endif %}
    //                                     </div>
    //                                     <div className="w-100 mt-n2">
    //                                         <h3 className="mb-0">
    //                                             <a href="#">{{ education.institution}} </a>
    //                                         </h3>
    //                                         <p>{{ education.description|safe }}<p>
    //                                         <div className="d-flex align-items-center justify-content-md-between flex-wrap">
    //                                             <p>{{ education.start_date}}- {{ education.end_date}}</p>
    //                                             <div>
    //                                             <a  href="{% url 'edit-education' education.pk %}" className="education-edit font-size-3">Edit</a>
    //                                             <a  style="color: red; margin-left: 20px" href="{% url 'delete education' education.pk %}" className="education-edit font-size-3">Delete</a>
    //                                             </div>
    //                                             </div>
    //                                     </div>
    //                                 </div>
    //                             </div>
    //                             {% endfor %} */}
    //                                                         </div>
    //                                                     </div>
    //                                                 </div>
    //                                             </div>
    //                                         </div>
    //                                     </div>
    //                                 </div>
    //                             </div>
    //                         </div>
    //                     </div>
    //                 </div>
    //             </div>
    //         </div>
    //     </>
    //
}
