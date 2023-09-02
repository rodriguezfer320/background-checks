import React from "react";
import Form from "./form.jsx";
import Table from "./table.jsx";
import Modal from "./modal.jsx";
import { fetchData } from "./../../../composables/backgroundCheckApi.js";
import {
    searchFieldValidator, titleFieldValidator, documentFieldValidator,
    stateFieldValidator, commentFieldValidator, documentFileFieldValidator
} from "./../../../composables/validators.js";
import { ConsultContext } from "./context.js";
import { messageError, messageSuccess } from "./../../../composables/alert.js";

export default class Consult extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            select: {
                dataForm: [
                    { "label": "Todos", "value": "todos" },
                    { "label": "Pendiente", "value": "pendiente" },
                    { "label": "Rechazado", "value": "rechazada" },
                    { "label": "Corregido", "value": "corregida" },
                    { "label": "Aprobado", "value": "aprobada" }
                ],
                dataEdit: [
                    { "label": "Rechazado", "value": "rechazada" },
                    { "label": "Aprobado", "value": "aprobada" }
                ]
            },
            consult: {
                data: {
                    state: "todos"
                },
                error: {},
                dataRes: [],
                pagination: {},
                isLoading: false
            },
            modal: {
                status: "",
                idModal: "",
                idRequest: 0,
                title: "",
                data: {},
                error: {},
                isLoading: false
            },
            handleSubmit: this.handleSubmit.bind(this),
            handleChange: this.handleChange.bind(this),
            handleBlur: this.handleBlur.bind(this),
            consultDataTable: this.consultDataTable.bind(this),
            showModal: this.showModal.bind(this),
            hideModal: this.hideModal.bind(this)
        };

        this.abortController = new AbortController();
    }

    componentDidMount() {
        document
            .querySelector("#modalData")
            .addEventListener("hidden.bs.modal", this.state.hideModal);
        this.state.consultDataTable(null, 1);
    }

    componentWillUnmount() {
        if (this.state.consult.isLoading) {
            this.abortController.abort();
        }
    }

    consultDataTable(event, page) {
        if (event) { event.preventDefault(); }

        if (page) {
            this.setState(state => {
                state.consult.isLoading = true;
                state.consult.dataRes = [];
                state.consult.pagination = {};
                return state;
            });

            fetchData({
                endpoint: "/verificacion-solicitud",
                signal: this.abortController.signal,
                method: "GET",
                params: new URLSearchParams({
                    page,
                    state: this.state.consult.data.state,
                    search: this.state.consult.data.search ?? ""
                })
            }).then((resp) => {
                this.setState(state => {
                    state.consult.dataRes = resp.data;
                    state.consult.pagination = resp.pagination;
                    state.consult.isLoading = false;
                    return state;
                });
            }).catch((err) => {
                this.setState(state => {
                    state.consult.isLoading = false;
                    return state;
                });
                messageError(err, "No pudieron obtener las solicitudes de verificación");
            });
        }
    }

    handleSubmit(event) {
        let data = this.state.modal.data;
        const { idModal, idRequest } = this.state.modal;
        let urlName = "";
        let message = "";

        if (idModal === "modalEditData") {
            urlName = "datos";
            message = "No se pudo actualizar los datos de la solicitud";
        } else if (idModal === "modalEditState") {
            urlName = "estado";
            message = "No se pudo actualizar el estado de la solicitud";
        } else if (idModal === "modalEditDoc") {
            urlName = "documento";
            message = "No se pudo actualizar el documento de la solicitud";

            const dataTemp = new FormData();
            Object.keys(data).forEach((key) => {
                dataTemp.append(key, data[key]);
            });

            data = dataTemp;
        }

        this.setState(state => {
            state.modal.isLoading = true;
            return state;
        });

        fetchData({
            endpoint: `/verificacion-solicitud/editar-${urlName}/${idRequest}`,
            signal: this.abortController.signal,
            method: "PUT",
            data
        }).then((resp) => {
            this.setState(state => {
                state.modal.status = resp.data.status;
                state.modal.isLoading = false;
                return state;
            });
            messageSuccess(resp.data.message);
            document.getElementById("close-modal").click();
        }).catch((err) => {
            this.setState(state => {
                state.modal.isLoading = false;
                return state;
            });

            if (err.status === 422) {
                this.setState(state => {
                    state.modal.error = (idModal === "modalEditDoc") ? err.data.errors.files : err.data.errors.json;
                    return state;
                });
            } else {
                messageError(err, message);
            } 
        });
    }

    handleChange(event, actionMeta, tag) {
        const name = actionMeta ? actionMeta.name : event.target.name;
        const value = event.target ? (event.target.files ? event.target.files[0] : event.target.value) : event.value;
        this.setState(state => {
            state[tag]["data"][name] = value;
            return state;
        });
    }

    handleBlur(event, tag) {
        const isSelect = event.target.id === "consult-state" || event.target.id === "edit-state";
        const elem = isSelect ? event.target.closest("div.basic-single").querySelector("[name=state]") : event.target;
        const name = elem.name;
        const value = elem.files ? elem.files[0] : elem.value;
        this.validations(name, value, tag);
    }

    showModal(event) {
        const idModal = event.target.id;
        const data = Array.from(event.target.closest("tr").querySelectorAll("td"), td => td.textContent);

        this.setState(state => {
            state.modal.idModal = idModal;
            state.modal.idRequest = data[0];

            if (idModal === "modalViewPDF") {
                state.modal.title = `Documento de la solicitud #${data[0]}`;
                state.modal.data = {
                    enpoint: `/verificacion-solicitud/file/${data[0]}`
                };
            } else if (idModal === "modalEditData") {
                state.modal.title = `Editar datos de la solicitud #${data[0]}`;
                state.modal.data = {
                    title: data[2],
                    document: data[1]
                };
            } else if (idModal === "modalEditState") {
                state.modal.title = `Editar estado de la solicitud #${data[0]}`;
                state.modal.data = {
                    state: (data[4] === "aprobada" || data[4] === "rechazada") ? data[4] : "",
                    comment: data[3]
                };
            } else if (idModal === "modalEditDoc") {
                state.modal.title = `Cambiar documento de la solicitud #${data[0]}`;
                state.modal.data = {};
            }

            return state;
        });
    }

    hideModal(event) {
        if (this.state.modal.status === "SUCCESS") {
            if (this.state.modal.idModal !== "modalEditDoc") {
                const keys = Object.keys(this.state.modal.data);
                keys.forEach((key, index) => {
                    const elem = document.getElementById(key + "-" + this.state.modal.idRequest);
                    if (elem) { elem.textContent = this.state.modal.data[keys[index]]; }
                });
            } else {
                document.getElementById("modalEditDoc").remove();
                document.getElementById("state-" + this.state.modal.idRequest).textContent = "corregida";
            }
        }

        this.setState(state => {
            state.modal.status = "";
            state.modal.idModal = "";
            state.modal.idRequest = 0;
            state.modal.title = "";
            state.modal.data = {};
            state.modal.error = {};
            return state;
        });
    }

    validations(name, value, tag) {
        let message = null;

        if (name === "search") {
            message = searchFieldValidator(value);
        } else if (name === "title") {
            message = titleFieldValidator(value);
        } else if (name === "document") {
            message = documentFieldValidator(value);
        } else if (name === "state") {
            message = stateFieldValidator(value);
        } else if (name === "comment") {
            message = commentFieldValidator(value);
        } else if (name === "file_document") {
            message = documentFileFieldValidator(value);
        }

        this.setState(state => {
            state[tag]["error"][name] = message;
            return state;
        });
    }

    render() {
        return (
            <ConsultContext.Provider value={this.state}>
                <div className="page_header pb-2 mt-4 mb-2">
                    <h1>consultar solicitudes de verificación</h1>
                    <hr className="bg-primary hr_title" />
                </div>
                <div className="row">
                    <Form />
                    <Table />
                    <Modal />
                </div>
            </ConsultContext.Provider>
        );
    }
};