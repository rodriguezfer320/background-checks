export const getRefreshToken = () => {
    return localStorage.getItem("refresh_token");
}

export const getAccessToken = () => {
    return localStorage.getItem("access_token");
}

export const getUser = () => {
    return localStorage.getItem("user");
}

export const getUserDocument = () => {
    return localStorage.getItem("user_document");
}

export const getUserName = () => {
    return localStorage.getItem("user_name");
}

export const getProfilePicture = () => {
    return localStorage.getItem("profile_picture") || (process.env.PUBLIC_URL + "/default-user-avatar.png");
}

export const getUserRole = () => {
    return localStorage.getItem("role");
}

export const validateRole = (allowedRoles) => {
    const userRole = getUserRole();
    return (allowedRoles && userRole) ? allowedRoles.includes(userRole) : false;
}