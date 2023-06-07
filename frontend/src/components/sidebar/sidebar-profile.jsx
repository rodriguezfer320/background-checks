import React from "react";
import { getProfilePicture, getUserName, getUserRole } from "./../../composables/sessionData.js";

class SidebarProfile extends React.Component {
	render() {
		return (
			<div className="menu">
				<div className="menu-profile">
					<div className="menu-profile-link">
						<div className="menu-profile-cover with-shadow"></div>
						<div className="menu-profile-image">
							<img src={getProfilePicture()} alt="avatar del usuario" />
						</div>
						<div className="menu-profile-info">
							<div className="d-flex align-items-center">
								<div className="flex-grow-1">{getUserName()}</div>
							</div>
							<small>{getUserRole()}</small>
						</div>
					</div>
				</div>
			</div>
		);
	}
}

export default SidebarProfile;