import React from "react";
import { BrowserRouter, Routes, Route, Outlet, Navigate } from "react-router-dom";
import App from "./../app.jsx";
import Login from "./../pages/login/login.jsx";
import ConsultBackground from "./../pages/background-checks/consult-background.jsx";
import CreateRequest from "./../pages/verification-request/create-request.jsx";
import ConsultRequest from "./../pages/verification-request/consult-request/consult.jsx";
import ErrorPage from "./../pages/errors/error-page.jsx";
import { getRefreshToken, validateRole } from "./../composables/sessionData.js";
import { Roles } from "./../composables/config.js";

function Authenticated() {
	return getRefreshToken() ? <App /> : <Navigate to="/login" replace />;
}

function RoleProtected({ allowedRoles }) {
	return validateRole(allowedRoles) ? <Outlet /> : <ErrorPage code="403" />;
}

function AppRoute() {
	return (
		<BrowserRouter basename="fs-uv/bc">
			<Routes>
				<Route exact path="login" element={<Login />} />
				<Route element={<Authenticated />}>
					<Route exact path="verificacion-antecedentes" element={<RoleProtected allowedRoles={[Roles.company]} />}>
						<Route path="consultar-antecedentes" element={<ConsultBackground />} />
						<Route path="" element={<ErrorPage code="404" />} />
					</Route>
					<Route exact path="verificacion-solicitud">
						<Route element={<RoleProtected allowedRoles={[Roles.candidate]} />}>
							<Route path="crear" element={<CreateRequest />} />
							<Route path="consultar-candidato" element={<ConsultRequest />} />
						</Route>
						<Route element={<RoleProtected allowedRoles={[Roles.officer]} />}>
							<Route path="consultar-funcionario" element={<ConsultRequest />} />
						</Route>
						<Route path="" element={<ErrorPage code="404" />} />
					</Route>
					<Route path="*" element={<ErrorPage code="404" />} />
				</Route>
				<Route path="*" element={<Navigate to="/login" replace />} />
			</Routes>
		</BrowserRouter>
	);
}

export default AppRoute;
