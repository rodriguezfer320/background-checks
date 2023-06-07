//import axios from "axios";

export const logout = async (event) => {
    /*const response = await axios({
        url: `${process.env.REACT_APP_AUTH_BACKEND_URL}/auth/api/logout/`,
        method: "POST",
        data: { "refresh_token": localStorage.getItem("refresh_token") },
    })
        .catch((err) => {
            return err.response
        });
    if (response.status === 205) {
        localStorage.clear()
        return response.data
    }
    else {
        return undefined
    }*/
    event.preventDefault();
    localStorage.clear();
	window.location = "/fs-uv/login";
};

export const refreshToken = async () => {
    /*const response = await axios({
        url: `${process.env.REACT_APP_AUTH_BACKEND_URL}/auth/api/refresh/`,
        method: "POST",
        data: { 'refresh': localStorage.getItem("refresh_token") },
    })
        .catch((err) => {
            return err.response
        });
    if (response.status === 200) {
        return response.data
    }
    else {
        return undefined
    }*/
};