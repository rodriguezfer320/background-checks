import axios from "axios";
import Swal from "sweetalert2";
import { getAccessToken, getRefreshToken } from "./sessionData.js";
import { fetchDataAuth } from "./authenticationApi.js";

const api = axios.create({
    baseURL: "http://localhost:8001/fs-uv/bc/api"
});

api.interceptors.request.use(config => {
    if (config.data !== null && !(config.data instanceof FormData)) {
        Object.assign(config.headers, { "Content-Type": "application/json" });
    }
    Object.assign(config.headers, { "Authorization": "Bearer " + getAccessToken() });
    return config;
});

api.interceptors.response.use(
    (response) => {
        let respData = response.data;
        let data = respData;
        let pagination = {};

        if (respData.data) {
            data = respData.data;

            if (respData.pagination) {
                pagination = respData.pagination;
            }
        }
        
        return {
            data: data,
            pagination: pagination,
            status: response.status
        };
    }, async (error) => {
        if (error.response) {
            // se decodifica la respuesta enviada a json
            if (error.config.responseType === "arraybuffer") {
                const uintArray = new Uint8Array(error.response.data);
                const encodedString = String.fromCharCode.apply(null, uintArray);
                const data = JSON.parse(encodedString);
                error.response.data = data;
            }

            // se refresca el token cuando ha expirado 
            if (error.response.status === 401 && error.response.data.status === "TOKEN NOT VALID") {
                const responseRefreshToken = await fetchDataAuth({
                    endpoint: "api/refresh/", 
                    method: "POST", 
                    data: {
                        "refresh": getRefreshToken()
                    }
                });

                // se actualiza el token y se vuelve a realizar la petición del usuario
                if(responseRefreshToken.status === 200) {
                    localStorage.setItem("access_token", responseRefreshToken.data.access);
                    return await api(error.config);
                } 

                // se cierra la sesión del usuario
                await Swal.fire({
                    title: "Sesión Caducada",
                    text: "Ha expirado su sesión, si desea continuar en la aplicación vuelva a iniciar sesión.",
                    icon: "info",
                    confirmButtonText: "OK",
                    confirmButtonColor: "#2d353c"
                }).then(() => {
                    localStorage.clear();
                    window.location = "/fs-uv/bc/login";
                });

                error = responseRefreshToken;
                error.status = "ERR_SESSION_EXPIRED";
            } else {
                error = {
                    data: error.response.data, 
                    status: error.response.status,
                    statusText: error.response.statusText,
                };
            }
        } else {
            error = {
                status: error.code,
                statusText: error.message
            };  
        }

        return Promise.reject(error);
    }
);

export const fetchData = async ({ endpoint, signal = null, method, data = null, params = null, responseType = "json" }) => {
    return await api({ signal, method, url: endpoint, data, params, responseType });
};