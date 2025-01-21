import React from 'react';
import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const navigate = useNavigate();
    const handleLogin = () => {
        // Send login request to the backend
        axios
        .post(`${process.env.REACT_APP_BACKEND_URL}/login`, { email, password })
        .then(response => {
            setMessage(response.data.message);
            const { email, token } = response.data;
            localStorage.setItem('username', email);
            localStorage.setItem('token', token);
            // Redirect to homepage using navigate
            navigate('/'); // Replace '/' with the homepage URL if needed
        })
        .catch(error =>
            {
                console.error(error);
                setMessage('Error logging in. Please try again.');
            });
        };
        // TODO: DRY up with Register
        return (
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
                    <button className="formButton" onClick={handleLogin}>Login</button>
                    {message && <p>{message}</p>}
                </div>
            </div>
        );
    }
    export default Login;