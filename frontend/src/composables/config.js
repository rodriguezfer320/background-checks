export const Roles = {
    company: "company",
    candidate: "student",
    officer: "program_direction"
};

export let Redirect = {};
Redirect[Roles.company] = "/verificacion-antecedentes/consultar-antecedentes";
Redirect[Roles.candidate] = "/verificacion-solicitud/consultar-candidato";
Redirect[Roles.officer] = "/verificacion-solicitud/consultar-funcionario";

export const BaseUrlFrontLogin = "https://fsu-front.vercel.app";