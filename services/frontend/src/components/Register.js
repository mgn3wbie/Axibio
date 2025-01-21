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
        .post('http://localhost:8000/register', { email, password })
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
        <div>
        <h2>Register</h2>
        <div>
        <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={e => setEmail(e.target.value)}
        />
        <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={e => setPassword(e.target.value)}
        />
        <button onClick={handleRegister}>Register</button>
        {message && <p>{message}</p>}
        </div>
        </div>
    );
}
export default Register;