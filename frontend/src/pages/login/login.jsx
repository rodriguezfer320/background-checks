import React from 'react';

class Login extends React.Component {
	constructor(props) {
		super(props);
		this.handleClick = this.handleClick.bind(this);
	}

	handleClick(event) {
		const user = {
			'document': '1118310093',
			'role': 'empresa'
		}
		const redirect = {
			'empresa': '/verificacion-antecedentes/consultar-antecedentes',
			'candidato': '/verificacion-solicitud/consultar-candidato',
			'admin': '/verificacion-solicitud/consultar-funcionario'
		}

		localStorage.setItem('user', JSON.stringify(user));
		window.location = redirect[user.role];
	}

	render() {
		return (
			<>
				<h1>Login</h1>
				<button onClick={this.handleClick}>Ingresar</button>
			</>
		)
	}
}

export default Login;