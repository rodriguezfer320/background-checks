import axios from "axios";
import { getAccessToken } from "./sessionData.js";
import { Roles } from "./config.js";

const api = axios.create();

api.interceptors.response.use(
    (response) => {
        return {
            data: response.data, 
            status: response.status
        };
    }, (error) => {
        if (error.response) {
            error = {
                data: error.response.data, 
                status: error.response.status,
                statusText: error.response.statusText
            };
        } else {
            error = {
                data: error.message,
                status: error.code
            };  
        }
        
        return error;
    }
);

export const fetchDataProfile = async ({ method, userRole}) => {
    const config = {
        method,
        headers: {
            authorization: "Bearer " + getAccessToken()
        }, 
        baseURL: (userRole === Roles.candidate) ? "https://dolphin-app-5gjh6.ondigitalocean.app" : "https://fsu-backend-company-jrkhn.ondigitalocean.app",
        url: ((userRole === Roles.candidate) ? "/portfolio/student" : "/fs-uv/api/company") + "/get_pfp/", 
    };

    return await api(config);
};