export const getUser = () => {
    return JSON.parse(localStorage.getItem("user"));
}

export const getRole = () => {
    const user = getUser();
    return (user && user.role) ? user.role : "";
}

export const getDocument = () => {
    const user = getUser();
    return (user && user.document) ? user.document : "";
}

export const validateRole = (allowedRoles) => {
    const userRole = getRole();
    return (allowedRoles && userRole) ? allowedRoles.includes(userRole) : false;
}