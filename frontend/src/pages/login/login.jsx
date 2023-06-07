import React from "react";
import Select from "react-select";

class Login extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			options: [
				{"value": "company", "label": "empresa"},
				{"value": "student", "label": "candidato"},
				{"value": "officer", "label": "funcionario"}
			],
			redirect: {
				'company': '/fs-uv/verificacion-antecedentes/consultar-antecedentes',
				'student': '/fs-uv/verificacion-solicitud/consultar-candidato',
				'officer': '/fs-uv/verificacion-solicitud/consultar-funcionario'
			},
			role: "company"
		};
		this.handleChange = this.handleChange.bind(this);
		this.handleClick = this.handleClick.bind(this);
	}

	handleChange(data) {
		this.setState(state => {
			state.role = data.value;
			return state;
		});
	}

	handleClick(event) {
		localStorage.setItem('refresh_token', 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4NzIyMzQ5OCwiaWF0IjoxNjg1OTI3NDk4LCJqdGkiOiI0NTc1YzQ2N2RiNzI0MTQ1YWE5ZjY3NmVlMjA0Mjc5MiIsInVzZXJfaWQiOjE4LCJzdWJfa2V5IjoiNjIyOGEzNTAtOTljOS00NWUxLWE2ZDUtOWM4YTBiNmU4YjQxIiwicm9sZSI6InN0dWRlbnQifQ.aoXvtR2i8_x36DyhF81xeEJ5dIDhjQYJMcY1N6L4WEE1HdvzSE7Vm-ZgauyrXpN9oIkiUALyZY4pvXQwZIDi5qyx5-vvRldTIaI-qu4oDiN5Cg7fIXKaHdLjmgx7vj8AtoBFyO0Xbvmk51f-aSNXpKyXm0fsFtkFyEi8ieqeuNCkLOyJRIPK3cyJcS1f1qzYnQ_tSDUQmPCe2lNimdupt4pFPy84-DYdJQSa-Bl-z_cpYKI4Bqla1vypBZCtS2kttabIHKzNcs-DKcSx7WySulYdYaICMrITu_qlEa4VqfELjuC8k5eddx6k_w2hf-IQCou6morVdmtJ54y1L_35XA');
		localStorage.setItem('access_token', 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg1OTI4MTU4LCJpYXQiOjE2ODU5Mjc0OTgsImp0aSI6IjJlOTQxYjkyNTYzZTRhZTI4MzgwMjhjMWI3NjUwZDI2IiwidXNlcl9pZCI6MTgsInN1Yl9rZXkiOiI2MjI4YTM1MC05OWM5LTQ1ZTEtYTZkNS05YzhhMGI2ZThiNDEiLCJyb2xlIjoic3R1ZGVudCJ9.rC1BdFEjmo8vJKzQvwpgjmqdjcvFXdBZfnDZMLHbrltG5S6LOBsRI2YX-0BP18pmEcuYTHXJt1OBLL9wdjFu357_KEDjY5ByAbL2-TTP18fdVcGA0Rt_yRzSCWpoWQUjwWU74mhWZCoFQk7tLU0B5VdS577fc4sjqYXwT8QcvnSZ4y-abdAdlL7ECj-3YQRPqAtRFcaZ6SXB0E9_rXfc7XZnKCEHUluve2bqTL8q2KifBlm1w77t9eSMQjY0-GLybR95RpohaLkF9MDxmcV-H_Ia8unaZZdlk6xlQdKtmbGDi8X8CrG76gwS78nRLORd310dW2MIive6GnQOOa7hFw');
		localStorage.setItem('user', 'miguel.fernandez@correounivalle.edu.co');
		localStorage.setItem('user_document', '1118310093');
		localStorage.setItem('user_name', 'Anonimo xj');
		localStorage.setItem('profile_picture', '');
		localStorage.setItem('role', this.state.role);
		window.location = this.state.redirect[this.state.role];
	}

	render() {
		return (
			<>
				<h1>Login</h1>
				<Select
					inputId="role"
					name="role"
					defaultValue={this.state.options[0]}
					className="basic-single"
					classNamePrefix="select"
					placeholder="Seleccione un rol"
					options={this.state.options}
					onChange={this.handleChange}
				/>
				<button onClick={this.handleClick}>Ingresar</button>
			</>
		);
	}
};

export default Login;