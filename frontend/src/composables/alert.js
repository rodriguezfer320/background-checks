import Swal from "sweetalert2";

export const messageError = (error, text, title="Fallo") => {
    if (error.status !== "ERR_CANCELED" && error.status !== "ERR_SESSION_EXPIRED") {
        console.log(error)
        Swal.fire({
            title,
            text,
            icon: "error",
            confirmButtonText: "OK",
            confirmButtonColor: "#2d353c",
            footer: "Detalle: " + ((error.data) ? "Error "  + error.data.code : error.statusText)
        });
    }
};

export const messageSuccess = (title, text) => {
    Swal.fire({
        title,
        text,
        icon: "success",
        confirmButtonText: "OK",
        confirmButtonColor: "#2d353c"
    });
};