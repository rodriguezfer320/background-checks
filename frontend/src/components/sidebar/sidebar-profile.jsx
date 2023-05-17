import React from "react";

class SidebarProfile extends React.Component {

	render() {
		return (
			<div className="menu">
				<div className="menu-profile">
					<div className="menu-profile-link">
						<div className="menu-profile-cover with-shadow"></div>
						<div className="menu-profile-image">
							<img src="../assets/img/user/user-13.jpg" alt="" />
						</div>
						<div className="menu-profile-info">
							<div className="d-flex align-items-center">
								<div className="flex-grow-1">
									Sean Ngu
								</div>
							</div>
							<small>Front end developer</small>
						</div>
					</div>
				</div>
			</div>
		)
	}
}

export default SidebarProfile;