import React from "react";
import { Routes, Route, Outlet, Navigate } from "react-router-dom";
import App from "../app.jsx";
import Login from "../pages/login/login.jsx";
import ConsultBackground from "../pages/background-checks/consult-background.jsx";
import CreateRequest from "../pages/verification-request/create-request.jsx";
import ConsultRequest from "../pages/verification-request/consult-request/consult.jsx";
import PageNotFound from "../pages/errors/page-not-found.jsx";
import { getUser, validateRole } from "../composables/userData.js";
import { Roles } from "../composables/config.js";

function Authenticated() {
	return getUser() ? <Outlet /> : <Navigate to="/login" />;
}

function RoleProtected({ allowedRoles }) {
	return validateRole(allowedRoles) ? <Outlet /> : <PageNotFound />;
}

function AppRoute() {
	return (
		<Routes>
			<Route path="login" element={<Login />} />
			<Route element={<Authenticated />}>
				<Route element={<App />}>
					<Route path="verificacion-antecedentes" element={<RoleProtected allowedRoles={[Roles.company]} />}>
						<Route path="consultar-antecedentes" element={<ConsultBackground />} />
						<Route path="" element={<PageNotFound />} />
					</Route>
					<Route path="verificacion-solicitud">
						<Route element={<RoleProtected allowedRoles={[Roles.candidate]} />}>
							<Route path="crear" element={<CreateRequest />} />
							<Route path="consultar-candidato" element={<ConsultRequest />} />
						</Route>
						<Route element={<RoleProtected allowedRoles={[Roles.officer]} />}>
							<Route path="consultar-funcionario" element={<ConsultRequest />} />
						</Route>
						<Route path="" element={<PageNotFound />} />
					</Route>
					<Route path="*" element={<PageNotFound />} />
				</Route>
			</Route>
			<Route path="*" element={<Navigate to="/login" replace />} />
		</Routes>
	);
}

export default AppRoute;
