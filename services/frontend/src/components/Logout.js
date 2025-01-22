import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../utils/AuthContext';

function Logout() {
    const { logout } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        // Clear localStorage and navigate to /
        logout(false);
        navigate('/');
    }, [navigate]); // Run this effect once on component load

    return (
        <div>
            Logging out...
        </div>
    );
}
export default Logout;