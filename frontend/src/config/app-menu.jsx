import { Roles } from "./../composables/config.js";

const Menu = [
  {
    path: "/verificacion-antecedentes/", icon: "fas fa-magnifying-glass", title: "Verificación de antecedentes", allowedRoles: [Roles.company],
    children: [
      { path: "consultar-antecedentes", title: "Consultar antecedentes" }
    ]
  },
  {
    path: "/verificacion-solicitud/", icon: "fas fa-file", title: "Verificación de solicitud", allowedRoles: [Roles.candidate],
    children: [
      { path: "crear", title: "Crear solicitud" },
      { path: "consultar-candidato", title: "Consultar solicitudes" }
    ]
  },
  {
    path: "/verificacion-solicitud/", icon: "fas fa-file", title: "Verificación de solicitud", allowedRoles: [Roles.officer],
    children: [
      { path: "consultar-funcionario", title: "Consultar solicitudes" }
    ]
  }
];

export default Menu;