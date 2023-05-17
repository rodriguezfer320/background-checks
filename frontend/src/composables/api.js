import axios from "axios";
import { ApiBaseRoute } from "./config.js";

const api = axios.create({
    baseURL: ApiBaseRoute
});

api.interceptors.request.use(config => {
    if (config.data !== null && !(config.data instanceof FormData)) {
        Object.assign(config.headers, { "Content-Type": "application/json" });
    }
    console.log(config)
    return config;
});

api.interceptors.response.use(response => {
    return response.data;
}, error => {
    return Promise.reject(error);
});

export const fetchData = async ({ endpoint, signal, method, data = null, params = null }) => {
    return await api({ signal, method, url: endpoint, data, params });
};