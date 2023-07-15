import React from "react";
import { Navigate } from "react-router-dom";
import { getRefreshToken, redirectUser } from "./../../composables/sessionData.js";
import { fetchDataAuth } from "./../../composables/authenticationApi.js";
import { fetchDataProfile } from "./../../composables/profileApi.js";
import { Roles, BaseUrlFrontLogin } from "./../../composables/config.js";
import RegisterBg from "./../../assets/img/login/register-bg.png";
import logoUnivalle from "./../../assets/img/login/logo-univalle.png";

// css
import "./../../assets/css/login.css";

class Login extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			form: {
				data: {},
				error: {}
			},
			redirect: getRefreshToken() ? true : false 
		};
		this.handleChange = this.handleChange.bind(this);
		this.handleLogin = this.handleLogin.bind(this);
	}

	handleChange(event) {
		const id = event.target.id;
		const value = event.target.value;
		this.setState(state => {
			state.form.data[id] = value;
			return state;
		});
	}

	async handleLogin(event) {
		event.preventDefault();
		const refreshToken = this.state.form.data["refresh_token"];

		this.setState(state => {
			state.form.error = {};
			return state;
		});
		
		try {
			const responseDecodeToken = await fetchDataAuth({ 
				endpoint: "/user/decode_jwt/",
				method: "POST",
				data: {
					"auth-token": refreshToken
				}
			});

			const responseToken = await fetchDataAuth({ 
				endpoint: "api/refresh/",
				method: "POST",
				data: {
					"refresh": refreshToken
				}
			});
			
			if (responseDecodeToken.status === 200 && responseToken.status === 200) {
				const userRole = responseDecodeToken.data.role;
				localStorage.setItem("access_token", responseToken.data.access);
				localStorage.setItem("refresh_token", refreshToken);
				localStorage.setItem("role", userRole);
				localStorage.setItem("user_sub_key", responseDecodeToken.data.sub_key);
				
				const responseUserInfo = await fetchDataAuth({ 
					endpoint: "/user/get_user_basic_info/",
					method: "GET",
					auth: true
				});

				if (responseUserInfo.status === 200) {					
					localStorage.setItem("user_name", responseUserInfo.data.user_name);
					localStorage.setItem("user_last_name", responseUserInfo.data.user_last_name);				
				} else {
					console.log("Error al obtener los datos del usuario. Estado: " + responseUserInfo.status);
				}

				if (userRole === Roles.candidate || userRole === Roles.company) {
					const responseProfilePicture = await fetchDataProfile({
						method: "GET",
						userRole
					});
	
					if (responseProfilePicture.status === 200) {
						localStorage.setItem("profile_picture", "https://res.cloudinary.com/dlhcdji3v/" + responseProfilePicture.data.profile_picture);
					} else {
						console.log("Error al obtener la foto de perfil del usuario. Estado: " + responseProfilePicture.status);
					}
				}

				this.setState(state => {
					state.redirect = true;
					return state;
				});
			} else {
				let message = ""

				if(responseDecodeToken.status === 200) {
					message = (responseDecodeToken.data) ? responseToken.data.detail : "Error: " + responseToken.status;
				} else {
					message = (responseDecodeToken.data) ? responseDecodeToken.data : "Error: " + responseDecodeToken.status;
				}

				this.setState(state => {
					state.form.error["refresh_token"] = message;
					return state;
				});
			}
		} catch (err) {
			console.log("Error login");
			console.log(err);
		}
	}

	render() {
		if (this.state.redirect) {
			return <Navigate to={redirectUser()} replace />;
		}

		return (
			<div className="login login-with-news-feed">
				<div className="news-feed">
					<div className='news-image'> 
						<img src={RegisterBg} alt="register-bg" className='bg-style'/>
					</div>
					<div className="news-caption">
						<h4 className="caption-title"><b>Finishing Schools</b> Univalle</h4>
						<p>
							Servicio de verificación de antecedentes
						</p>
					</div>
				</div>
				<div className="login-container">
					<div className="register-header mb-25px h1">
						<div className='col-lg-12 col-md-12 col-sm-12 col-xs-9'>
							<img className='logo' src={logoUnivalle} style={{"width":"80%","marginBottom": '12px'}} alt="bg-register"/>
						</div>
					</div>
					<div className="text-gray pb-4">
						<b>¡Bienvenido!</b> Inicia sesión <a href={BaseUrlFrontLogin} target="_blank" rel="noreferrer">aqui</a> 
						&nbsp; y recupera la sesión copiando el refresh token del local storage
					</div>
					<div className="login-content">
						<form onSubmit={this.handleLogin} className="fs-13px" autoComplete="off">
							<div className="form-floating">
								<input type="text" className="form-control h-45px fs-13px" 
								placeholder="Refresh token" id="refresh_token" onChange={this.handleChange}/>
								<label htmlFor="refresh_token" className="d-flex align-items-center fs-13px text-gray-600">Refresh token</label>
							</div>
							<div className="invalid-feedback" style={{"display": "flex"}}>
								{this.state.form.error.refresh_token ?? ""}
							</div>			
                            <div className="mb-4 mt-4">
                                <button type="submit" className="btn btn-primary d-block w-100 btn-lg h-45px fs-13px">Ingresar</button>
                            </div>
						</form>
					</div>
				</div>
			</div>
		);
	}
};

export default Login;