import React from "react";
import { Outlet } from "react-router-dom";
import { AppSettings } from "../../config/app-settings.js";

class Content extends React.Component {
	render() {
		return (
			<AppSettings.Consumer>
				{({ appContentClass }) => (
					<div id="app" className={"app app-content-full-height " + appContentClass}>
						<div id="content" className="app-content d-flex flex-column p-0">
							<div className="app-content-padding flex-grow-1 overflow-hidden" data-scrollbar="true" data-height="100%">
								<Outlet />
							</div>
							<div id="footer" className="app-footer m-0">
								&copy; Finishing School todos los derechos reservados 2023
							</div>
						</div>
					</div>
				)}
			</AppSettings.Consumer>
		);
	}
};

export default Content;