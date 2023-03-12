import React from 'react';

function Navbar() {
    return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
      <a className="navbar-brand" href="/">
        Drop-in
      </a>
      <buttonz
        className="navbar-toggler"
        type="button"
        data-toggle="collapse"
        data-target="#navbarNavDropdown"
        aria-controls="navbarNavDropdown"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span className="navbar-toggler-icon"></span>
      </buttonz>

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
          <li className="nav-item">
            <a className="nav-link" href="/login">
              Login
            </a>
          </li>
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