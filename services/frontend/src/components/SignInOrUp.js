import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
function SignInOrUp() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const navigate = useNavigate();
    const AuthAction = {
        LOGIN: "login",
        SIGNUP: "signup",
    };

    const handleLogin = (authAction) => {
        // prepare formdata as oauth2 in the backend expects it
        // oauth2 wants a username in the payload
        const formData = new FormData();
        formData.append('username', email);
        formData.append('password', password);
        // Send login request to the backend
        axios
        .post(`${process.env.REACT_APP_BACKEND_URL}${authAction === AuthAction.LOGIN ? "/login" : "/register"}` , formData)
        .then(response => {
            const token = response.data.token_type+" "+response.data.access_token;
            // save the token in local storage
            localStorage.setItem('token', token);
            navigate('/data');
        })
        .catch(error => {
            // handles everything that isnt 200->299
            if (error.response) {
                // Request has been sent and backend replied
                setErrorMessage(error.response.data.detail || "Error logging in.");
            } else if (error.request) {
                // Request sent, but no response
                setErrorMessage("No response from the server. Please try again.");
            } else {
                // Request couldnt be send
                setErrorMessage("Unexpected error occurred. Please try again.");
            }
        });
    };

    return (
        <div className="center-container">
            <div id="login-form">
                <h2>Sign Up or Log In</h2>
                <div className="form-group">
                    <label htmlFor="email">E-mail address</label>
                    <input
                    id="email"
                    type="email"
                    placeholder="example@email.com"
                    value={email}
                    onChange={e => setEmail(e.target.value)}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Password</label>
                    <input
                    type="password"
                    placeholder="*******"
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                    />
                </div>
                <div>
                    <button className="formButton" onClick={() => handleLogin(AuthAction.SIGNUP)} >Sign Up</button>
                    <button className="formButton" onClick={() => handleLogin(AuthAction.LOGIN)}>Log In</button>
                </div>
                {errorMessage && <p className="error">{errorMessage}</p>}
            </div>
        </div>
    );
}
export default SignInOrUp;