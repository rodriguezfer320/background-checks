import { Redirect } from './config.js';

export const getAccessToken = () => {
    return localStorage.getItem("access_token");
}

export const getRefreshToken = () => {
    return localStorage.getItem("refresh_token");
}

export const getUserRole = () => {
    return localStorage.getItem("role");
}

export const validateRole = (allowedRoles=[]) => {
    const userRole = getUserRole();
    return userRole ? ((allowedRoles.length > 0) ? allowedRoles.includes(userRole) : true) : false;
}

export const redirectUser = () => {
    const userRole = getUserRole();
    return userRole ? Redirect[userRole] : "/";
}

export const getUser = () => {
    return localStorage.getItem("user");
}

export const getUserSubKey = () => {
    return localStorage.getItem("user_sub_key");
}

export const getUserName = () => {
    return localStorage.getItem("user_name");
}

export const getProfilePicture = () => {
    return localStorage.getItem("profile_picture") || (process.env.PUBLIC_URL + "/assets/img/default-user-avatar.png");
}