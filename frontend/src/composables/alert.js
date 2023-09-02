import Swal from "sweetalert2";

export const messageError = (error, text, title="FALLO") => {
    if (error.status !== "ERR_CANCELED" && error.status !== "ERR_SESSION_EXPIRED") {
        let messageFooter = "Detalle: ";
        
        if (typeof error.data === 'object') {
            messageFooter += Number.isInteger(error.data.code) ? error.data.code : error.status
            messageFooter += ", "
            messageFooter += (error.data.detail) ? error.data.detail : error.data.message
        } else {
            messageFooter += error.status + ", "  + error.data
        }
        
        Swal.fire({
            title,
            text,
            icon: "error",
            confirmButtonText: "OK",
            confirmButtonColor: "#2d353c",
            footer: messageFooter
        });
    }
};

export const messageSuccess = (text, title='') => {
    Swal.fire({
        title: "ÉXITO",
        text,
        icon: "success",
        confirmButtonText: "OK",
        confirmButtonColor: "#2d353c"
    });
};