import React, {useEffect, useState} from "react";
import Breadcrumbs from "./Breadcrumbs";
import CandidatesAside from "./JobseekersAside";
import {Link} from "react-router-dom";

export default function JobseekersList() {
    const [candidates, setJobseekers] = useState([]);
    const [city, setCity] = useState("");

    useEffect(() => {
        const params = new URLSearchParams(window.location.search);
        const cityParam = params.get("city");
        if (cityParam) {
            setCity(cityParam);
        }
    }, []);

    useEffect(() => {
        fetch(`http://127.0.0.1:8000/candidate/candidates/?city=${city}`)
            .then((response) => response.json())
            .then((data) => setJobseekers(data));
    }, [city]);

    return (
        <>
            <Breadcrumbs pageTitle="Job Seekers" pageInfo="Find employees that match your hiring criteria." />

            <div className="manage-resumes section">
                <div className="container">
                    <div className="resume-inner">
                        <div className="row">
                            <div className="col-lg-8 col-12">
                                <div className="inner-content">
                                    {candidates.map((candidate) => (
                                        <div key={candidate.user} className="resume-item">
                                            <img src={`https://res.cloudinary.com/drjgddl0y/${candidate.profile_picture}`} alt="Candidate" />
                                            <div className="right">
                                                <h3>
                                                    <Link to={`/candidate/${candidate.user}`}>
                                                        {candidate.first_name} {candidate.last_name}
                                                    </Link>
                                                </h3>
                                                <span className="deg">{candidate.occupation}</span>
                                                <ul className="experience">
                                                    <li>
                                                        Seniority: <span>{candidate.seniority}</span>
                                                    </li>
                                                    <li>
                                                        GitHub:{" "}
                                                        <span>
                                                            <a target="_blank" href="{candidate.github}">
                                                                Link
                                                            </a>
                                                        </span>
                                                    </li>
                                                    <li>
                                                        <i className="lni lni-map-marker"></i>
                                                        {candidate.city}
                                                    </li>
                                                </ul>
                                                <ul className="skills">{/* Render candidate skills */}</ul>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                            <CandidatesAside />
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
}
