import React from "react";
import { AppSettings } from "../../config/app-settings.js";

class ErrorPage extends React.Component {
	static contextType = AppSettings;

	constructor(props) {
		super(props);

		this.state = {
			message: {
				"403": "Acceso denegado",
				"404": "Página no encontrada"
			},
			description: {
				"403": "La página a la que esta intentando acceder no esta permitida.",
				"404": "La página que esta buscando no existe."
			}
		}
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

	render() {
		return (
			<div className="error">
				<div className="error-code">{this.props.code}</div>
				<div className="error-content">
					<div className="error-message">{this.state.message[this.props.code]}</div>
					<div className="error-desc mb-4">{this.state.description[this.props.code]}</div>
				</div>
			</div>
		);
	}
}

export default ErrorPage;