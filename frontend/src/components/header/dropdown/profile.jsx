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
        event.stopPropagation();

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
				<div className="dropdown-menu dropdown-menu-end justify-content-center">
					<Link to="/" onClick={this.handleClick} className="dropdown-item">
						Log Out
						{this.state.isLoading
							? <div className="spinner-border spinner-border-sm" style={{ marginLeft: "60%" }} role="status">
								<span className="sr-only">Loading...</span>
							</div>
							: <></>
						}
					</Link>
				</div>
			</div>
		);
	}
};

export default DropdownProfile;