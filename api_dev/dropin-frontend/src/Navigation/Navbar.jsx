import React from 'react';
import {useSelector, useDispatch} from 'react-redux';
import {Navbar, Nav, Button} from 'react-bootstrap';

function MyNavbar() {
    const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);
    const dispatch = useDispatch();

    const handleLogout = () => {
        localStorage.clear();
        dispatch({type: 'LOGOUT'});
    };

    const loginLogout = isAuthenticated
        ? (
            <li className="nav-item" onClick={handleLogout}>
                <a className="nav-link" href="/">
                    Logout
                </a>
            </li>
        ) : (
            <li className="nav-item">
                <a className="nav-link" href="/login">
                    Login
                </a>
            </li>
        );

    return (
        <Navbar bg="transparent" expand="lg" className="mt-3 ms-3">
            <div className="container d-flex justify-content-center">
                <Navbar.Brand href="/" style={{fontSize: '1.5rem'}}>
                    Lilas
                </Navbar.Brand>
                <Navbar.Toggle aria-controls="navbarNavDropdown"/>
                <Navbar.Collapse id="navbarNavDropdown">
                    <Nav className="ms-auto">
                        <Nav.Link href="/manage-friends" className="text-dark">
                            Manage Friends
                        </Nav.Link>
                        <Nav.Link href="/map-view" className="text-dark">
                            Map View
                        </Nav.Link>
                        {loginLogout}
                        <Nav.Link href="/sign-up" className="btn btn-primary text-light">
                            Sign-up
                        </Nav.Link>
                    </Nav>
                </Navbar.Collapse>
            </div>
        </Navbar>
    );
}

export default MyNavbar;
