import React from "react";
import { Link } from "react-router-dom";
import DropdownProfile from "./dropdown/profile.jsx";
import { AppSettings } from "./../../config/app-settings.js";

class Header extends React.Component {

	render() {
		return (
			<AppSettings.Consumer>
				{({ toggleAppSidebarMobile, toggleAppSidebarEnd, toggleAppSidebarEndMobile, toggleAppTopMenuMobile, appHeaderMegaMenu, appHeaderInverse, appSidebarTwo, appTopMenu, appSidebarNone }) => (
					<div id="header" className={"app-header" + (appHeaderInverse ? " app-header-inverse" : "")}>
						<div className="navbar-header">
							{appSidebarTwo && (
								<button type="button" className="navbar-mobile-toggler" onClick={toggleAppSidebarEndMobile}>
									<span className="icon-bar"></span>
									<span className="icon-bar"></span>
									<span className="icon-bar"></span>
								</button>
							)}

							<Link to="#/" className="navbar-brand">
								<span className="navbar-logo"></span><b>FINISIHNG SCHOOLS</b>|Verificación de Antecedentes
							</Link>

							{appHeaderMegaMenu && (
								<button type="button" className="navbar-mobile-toggler" data-bs-toggle="collapse" data-bs-target="#top-navbar">
									<span className="fa-stack fa-lg text-inverse">
										<i className="far fa-square fa-stack-2x"></i>
										<i className="fa fa-cog fa-stack-1x"></i>
									</span>
								</button>
							)}

							{appTopMenu && !appSidebarNone && (
								<button type="button" className="navbar-mobile-toggler" onClick={toggleAppTopMenuMobile}>
									<span className="fa-stack fa-lg text-inverse">
										<i className="far fa-square fa-stack-2x"></i>
										<i className="fa fa-cog fa-stack-1x"></i>
									</span>
								</button>
							)}

							{appSidebarNone && appTopMenu && (
								<button type="button" className="navbar-mobile-toggler" onClick={toggleAppTopMenuMobile}>
									<span className="icon-bar"></span>
									<span className="icon-bar"></span>
									<span className="icon-bar"></span>
								</button>
							)}

							{!appSidebarNone && (
								<button type="button" className="navbar-mobile-toggler" onClick={toggleAppSidebarMobile}>
									<span className="icon-bar"></span>
									<span className="icon-bar"></span>
									<span className="icon-bar"></span>
								</button>
							)}
						</div>

						<div className="navbar-nav">
							<DropdownProfile />

							{appSidebarTwo && (
								<div className="navbar-divider d-none d-md-block"></div>
							)}

							{appSidebarTwo && (
								<div className="navbar-item d-none d-md-block">
									<Link to="/" onClick={toggleAppSidebarEnd} className="navbar-link icon">
										<i className="fa fa-th"></i>
									</Link>
								</div>
							)}
						</div>
					</div>
				)}
			</AppSettings.Consumer>
		);
	}
};

export default Header;