import axios from "axios";
import { getAccessToken } from "./sessionData.js";
import { Roles } from "./config.js";

const api = axios.create();

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