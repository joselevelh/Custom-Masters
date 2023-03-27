import React, {useEffect, useState} from 'react';
import jwtDecode from "jwt-decode"

function Navbar() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    useEffect(() => {
        try {
            const token = localStorage.getItem('accessToken')
            console.log('Has token:', token)
            const decoded = jwtDecode(token);

            if (decoded && decoded.exp && Date.now() < decoded.exp * 1000) {
                // Token is still valid
                setIsLoggedIn(true);
                console.log("User is logged in!")
            } else {
                // Token has expired or is invalid
                setIsLoggedIn(false);
                console.log("User is not logged in!")
            }
        } catch (e) {
            console.log(e)
        }
    }, []);
    let login_logout;
    const handleLogout = () => {
        // client.logout();
        setIsLoggedIn(false);
        localStorage.clear()
    }

    if (isLoggedIn) {
        login_logout = <li className="nav-item" onClick={() => handleLogout()}>
            <a className="nav-link" href="/">Logout</a>
        </li>;
    } else {
        login_logout = <li className="nav-item">
            <a className="nav-link" href="/login">
            Login
        </a></li>;
    }

    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
            <a className="navbar-brand" href="/">
                Drop-in
            </a>
            <div className="collapse navbar-collapse" id="navbarNavDropdown">
                <ul className="navbar-nav">
                    <li className="nav-item">
                        <a className="nav-link" href="/manage-friends">
                            Manage Friends
                        </a>
                    </li>
                    <li className="nav-item">
                        <a className="nav-link" href="/map-view">
                            Map View
                        </a>
                    </li>
                    {login_logout}
                    <li className="nav-item">
                        <a className="nav-link" href="/sign-up">
                            Sign-up
                        </a>
                    </li>
                </ul>
            </div>
        </nav>
    );
}

export default Navbar;