import React from "react";
import { Link } from "react-router-dom";
import { getProfilePicture, getUserName } from "./../../../composables/sessionData.js";
import { logout } from "./../../../composables/logout.js";

class DropdownProfile extends React.Component {

	render() {
		return (
			<div className="navbar-item navbar-user dropdown">
				<a href="#/" className="navbar-link dropdown-toggle d-flex align-items-center" data-bs-toggle="dropdown">
					<img src={getProfilePicture()} alt="avatar de usuario" />
					<span>
						<span className="d-none d-md-inline">{"Hola, " + getUserName()}</span>
						<b className="caret"></b>
					</span>
				</a>
				<div className="dropdown-menu dropdown-menu-end me-1">
					<Link to="/logout" className="dropdown-item" onClick={logout}>Salir</Link>
				</div>
			</div>
		);
	}
};

export default DropdownProfile;