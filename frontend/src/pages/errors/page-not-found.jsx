import React from "react";
import { AppSettings } from "../../config/app-settings.js";

class PageNotFound extends React.Component {
	static contextType = AppSettings;

	constructor(props) {
		super(props);
		this.handleClick = this.handleClick.bind(this);
	}

	componentDidMount() {
		this.context.handleSetAppSidebarNone(true);
		this.context.handleSetAppHeaderNone(true);
		this.context.handleSetAppContentClass("p-0");
		document.getElementById("footer").style.display = "none";
		document.querySelector("div[data-scrollbar=true]").className = "";
	}

	componentWillUnmount() {
		this.context.handleSetAppSidebarNone(false);
		this.context.handleSetAppHeaderNone(false);
		this.context.handleSetAppContentClass("");
		document.getElementById("footer").style.display = "";
		document.querySelector("div[data-scrollbar=true]").className = "app-content-padding flex-grow-1 overflow-hidden";
	}

	handleClick(event) {
		window.history.back();
	}

	render() {
		return (
			<div className="error">
				<div className="error-code">404</div>
				<div className="error-content">
					<div className="error-message">Página No Encontrada</div>
					<div className="error-desc mb-4">La página que busca no existe.</div>
					<div>
						<button onClick={this.handleClick} className="btn btn-success px-3">Regresar</button>
					</div>
				</div>
			</div>
		);
	}
}

export default PageNotFound;