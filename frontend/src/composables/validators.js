export const antecedentsFieldValidator = (antecedents) => {
    if (!antecedents || antecedents[0] === "") {
        return "Debe seleccionar al menos un antecedente.";
    }

    return null;
};

export const documentFieldValidator = (document) => {
    if (!document) {
        return "Debe ingresar el número de identificación.";
    } else if (!new RegExp(/^[0-9]{8,10}$/).test(document)) {
        return "Ingrese un número de identificación entre 8 y 10 digitos.";
    }

    return null;
};

export const titleFieldValidator = (title) => {
    if (!title) {
        return "Debe ingresar un titulo.";
    }

    return null;
};

export const antecedentFieldValidator = (antecedent) => {
    if (!antecedent) {
        return "Debe seleccionar un antecedente.";
    }

    return null;
};

export const documentFileFieldValidator = (file) => {
    if (!file) {
        return "Debe seleccionar un documento.";
    } else if (file.type !== "application/pdf") {
        return "Debe seleccionar un archivo en formato pdf.";
    } else if ((file.size / 1000000) > 10.0) {
        return "Debe seleccionar un archivo que no supere los 10Mb.";
    }

    return null;
};

export const searchFieldValidator = (search) => {
    if (!search) {
        return undefined;
    } else if (isNaN(parseInt(search))) {
        return "Ingrese solo numeros enteros.";
    }

    return null;
};

export const stateFieldValidator = (state) => {
    if (!state) {
        return "Debe seleccionar un estado.";
    }

    return null;
};

export const commentFieldValidator = (comment) => {
    if (!comment) {
        return "Debe ingresar un comentario.";
    }

    return null;
};