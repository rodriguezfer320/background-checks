import React from "react";
import { Link } from "react-router-dom";
import { getProfilePicture, getUserName } from "./../../../composables/sessionData.js";
import { logout } from "./../../../composables/logout.js";

class DropdownProfile extends React.Component {

	constructor(props) {
        super(props);
        this.state = {
            isLoading: false
        };
        this.handleClick = this.handleClick.bind(this);
    }

	async handleClick(event) {
		event.preventDefault();

		this.setState((state) => {
			state.isLoading = true;
			return state;
		});

		const status = await logout();

		this.setState((state) => {
			state.isLoading = status;
			return state;
		});
	}

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
				<div className="dropdown-menu dropdown-menu-end justify-content-center me-1">
					<Link to="/logout" className="dropdown-item" onClick={this.handleClick}>
						Log Out &nbsp;&nbsp;&nbsp;&nbsp;
						&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
						{this.state.isLoading && <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>}
					</Link>
				</div>
			</div>
		);
	}
};

export default DropdownProfile;