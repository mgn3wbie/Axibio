import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../utils/AuthContext';

function LogButtons() {
    const { isLoggedIn } = useAuth();

    if (isLoggedIn) {
        return (
            <div className="logbuttons">
                <Link to="/data"><button className="padded-button">See the data</button></Link>
            </div>
        );
    }
    return (
        <div className="logbuttons">
            <Link to="/auth"><button className="padded-button">Log In or Sign Up</button></Link>
        </div>
    );
}

function Homepage() {
    const [userData, setUserData] = useState(null);
    const { isLoggedIn } = useAuth();

    useEffect(() => {
        // avoid the request if no token is set
        if (!isLoggedIn) {
            return;
        }
        
        const token = localStorage.getItem('token');
        // Fetch user data from the API endpoint
        axios.get(`${process.env.REACT_APP_BACKEND_URL}/users/me`, {
            headers: {
                Authorization: token,
            },
        })
        .then(response => setUserData(response.data))
        .catch(error => {
            if (error.response.status === 401) {
                console.log("Unauthorized. You need to login...");
                localStorage.clear();
                setUserData(null);
            }
        });
    }, []);
    return (
        <div>
            <h1>Welcome to Axibio Technical Test</h1>
            
            {userData ? (
                <p id="homePageParagraph">
                    Hello {userData.username.substring(0, userData.username.indexOf('@'))}!
                </p>
            ) : (
                <p id="homePageParagraph">
                    You are not logged in. Please log in or sign up to continue.
                </p>
            )}
            
            <LogButtons />
        </div>
    );
}
export default Homepage;