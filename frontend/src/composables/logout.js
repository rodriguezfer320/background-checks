import { getRefreshToken } from "./sessionData.js";
import { fetchDataAuth } from "./authenticationApi.js";
import { messageError } from "./alert.js";

export const logout = async () => {
    try {
        const responseLogout = await fetchDataAuth({ 
            endpoint: "/api/logout/",
            method: "POST",
            data: {
                "refresh_token": getRefreshToken()
            }
        });
    
        if (responseLogout.status === 205 || (responseLogout.data && responseLogout.data.error === "Token is blacklisted")) {					
            localStorage.clear();
            window.location = "/fs-uv/bc/login";
        } else {
            messageError(responseLogout, "No se puedo cerrar la sesión debido aún fallo.");
        }
    } catch (err) {
        messageError(
            {
                status: err.name,
                data: err.message
            },
            "Error al cerrar la sesión"
        );
    } finally {
        return false;
    }
};