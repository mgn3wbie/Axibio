import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
function Register() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const navigate = useNavigate();
    const handleRegister = () => {
        // Send registration request to the backend
        axios
        .post(`${process.env.REACT_APP_BACKEND_URL}/register`, { email, password })
        .then(response => {
            setMessage(response.data.message);
            const { email, token } = response.data;
            // oauth2 wants a username in the payload
            localStorage.setItem('username', email);
            localStorage.setItem('token', token);
            // Redirect to homepage using navigate
            navigate('/'); // Replace '/' with the homepage URL if needed
        })
        .catch(error => {
            console.error(error);
            setMessage('Error registering. Please try again.');
        });
    };
    return (
        // TODO: DRY up with Login
        <div className="center-container">
                <div id="login-form">
                    <h2>Login</h2>
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
                    <button className="formButton" onClick={handleRegister}>Register</button>
                    {message && <p>{message}</p>}
                </div>
            </div>
    );
}
export default Register;