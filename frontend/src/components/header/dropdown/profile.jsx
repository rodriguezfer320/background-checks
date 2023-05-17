import React from "react";
import { getRole } from "../../../composables/userData.js";

class DropdownProfile extends React.Component {

	render() {
		return (
			<div className="navbar-item navbar-user dropdown">
				<a href="#/" className="navbar-link dropdown-toggle d-flex align-items-center" data-bs-toggle="dropdown">
					<img src={"../assets/img/user/user-13.jpg"} alt="" />
					<span>
						<span className="d-none d-md-inline">{"Hola, " + getRole()}</span>
						<b className="caret"></b>
					</span>
				</a>
				<div className="dropdown-menu dropdown-menu-end me-1">
					<a href="#/" className="dropdown-item">Salir</a>
				</div>
			</div>
		);
	}
};

export default DropdownProfile;