import axios from "axios";
import { getAccessToken } from "./sessionData.js";

const api = axios.create({
    baseURL: "https://fs-uv-auth-iavei.ondigitalocean.app/fs-uv/auth"
});

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

export const fetchDataAuth = async ({ endpoint, method, data=null, auth=false}) => {
    let config = { method, url: endpoint, data };

    if (auth) {
        config["headers"] = {
            authorization: "Bearer " + getAccessToken()
        };
    }

    return await api(config);
};