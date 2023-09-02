import React from "react";
import { Navigate } from "react-router-dom";
import { getRefreshToken, redirectUser } from "./../../composables/sessionData.js";
import { fetchDataAuth } from "./../../composables/authenticationApi.js";
import { fetchDataProfile } from "./../../composables/profileApi.js";
import { Roles, BaseUrlFrontLogin } from "./../../composables/config.js";
import { messageError } from "./../../composables/alert.js";

// img
import RegisterBg from "./../../assets/img/login/register-bg.png";
import logoUnivalle from "./../../assets/img/login/logo-univalle.png";

// css
import "./../../assets/css/login.css";

class Login extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			refresh_token: null,
			redirect: getRefreshToken() ? true : false 
		};
		this.handleChange = this.handleChange.bind(this);
		this.handleLogin = this.handleLogin.bind(this);
	}

	handleChange(event) {
		this.setState(state => {
			state.refresh_token = event.target.value;
			return state;
		});
	}

	async handleLogin(event) {
		event.preventDefault();
		
		try {
			// se decodifica el el refresh token
			const responseDecodeToken = await fetchDataAuth({ 
				endpoint: "/user/decode_jwt/",
				method: "POST",
				data: {
					"auth-token": this.state.refresh_token
				}
			});

			if (responseDecodeToken.status === 200) {
				// se obtiene un nuevo token
				const responseToken = await fetchDataAuth({ 
					endpoint: "api/refresh/",
					method: "POST",
					data: {
						"refresh": this.state.refresh_token
					}
				});

				if (responseToken.status === 200) {
					// se añaden los datos de la sesión requeridos al localstorage
					const userRole = responseDecodeToken.data.role;
					localStorage.setItem("access_token", responseToken.data.access);
					localStorage.setItem("refresh_token", this.state.refresh_token);
					localStorage.setItem("role", userRole);
					
					// se obtiene información del usuario
					const responseUserInfo = await fetchDataAuth({ 
						endpoint: "/user/get_user_basic_info/",
						method: "GET",
						auth: true
					});
	
					if (responseUserInfo.status === 200) {					
						localStorage.setItem("user_name", responseUserInfo.data.user_name);
						localStorage.setItem("user_last_name", responseUserInfo.data.user_last_name);				
					} else {
						messageError(
							responseUserInfo,
							"Error al obtener los datos del usuario"
						);
					}
	
					if (userRole === Roles.candidate || userRole === Roles.company) {
						// se obtiene la foto del perfil de usuario
						const responseProfilePicture = await fetchDataProfile({
							method: "GET",
							userRole
						});
		
						if (responseProfilePicture.status === 200) {
							if (responseProfilePicture.data.profile_picture) {
								localStorage.setItem("profile_picture", "https://res.cloudinary.com/dlhcdji3v/" + responseProfilePicture.data.profile_picture);
							}
						} else {
							messageError(
								responseProfilePicture,
								"Error al obtener la foto de perfil del usuario"
							);
						}
					}
	
					this.setState(state => {
						state.redirect = true;
						return state;
					});
				} else {
					messageError(
						responseToken,
						"Error al obtener un nuevo token"
					);
				}
			} else {
				messageError(
					responseDecodeToken,
					"Error al decodificar el refresh token"
				);
			}
		} catch (err) {
			messageError(
				{
					status: err.name,
					data: err.message
				},
				"Error al recuperar la sesión"
			);
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