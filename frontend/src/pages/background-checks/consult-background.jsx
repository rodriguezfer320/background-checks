import React, { Component } from "react";
import Select from "react-select";
import { Panel, PanelHeader, PanelBody } from "./../../components/panel/panel.jsx";
import ViewPDF from "./../../components/pdf/view-pdf.jsx";
import { fetchData } from "./../../composables/backgroundCheckApi.js";
import { documentFieldValidator, antecedentsFieldValidator } from "./../../composables/validators.js";
import { messageError } from "./../../composables/alert.js";

export default class ConsultBackground extends Component {

    constructor(props) {
        super(props);
        this.state = {
            select: {
                data: [],
                isLoading: false
            },
            consult: {
                data: [],
                isLoading: false
            },
            form: {
                data: {},
                error: {}
            },
            modal: {
                title: "",
                link: ""
            }
        };

        this.abortController = new AbortController();
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.handleBlur = this.handleBlur.bind(this);
        this.showModal = this.showModal.bind(this);
        this.hideModal = this.hideModal.bind(this);
    }

    componentDidMount() {
        this.setState(state => {
            state.select.isLoading = true;
            return state;
        });

        fetchData({
            endpoint: "/antecedentes",
            signal: this.abortController.signal,
            method: "GET"
        }).then((resp) => {
            this.setState((state) => {
                state.select.data = resp.data;
                state.select.isLoading = false;
                return state;
            });
        }).catch((err) => {
            this.setState(state => {
                state.select.isLoading = false;
                return state;
            });
            messageError(err, "No se pudieron cargar los antecedentes en el select");
        });

        document
            .querySelector("#modalViewPDF")
            .addEventListener("hidden.bs.modal", this.hideModal);
    }

    componentWillUnmount() {
        if (this.state.select.isLoading || this.state.consult.isLoading) {
            this.abortController.abort();
        }
    }

    handleSubmit(event) {
        event.preventDefault();
        const errors = [
            this.state.form.error.antecedents,
            this.state.form.error.document
        ];

        if (errors.includes(undefined)) {
            const keys = ["antecedents", "document"];

            errors.forEach((elem, index) => {
                if (elem === undefined) {
                    this.validations(keys[index], this.state.form.data[keys[index]]);
                }
            });
        } else if (!errors.some((v) => v !== null)) {
            const { document, antecedents } = this.state.form.data;

            this.setState((state) => {
                state.consult.data = [];
                state.consult.isLoading = true;
                return state;
            });

            fetchData({
                endpoint: "/verificacion-antecedentes",
                signal: this.abortController.signal,
                method: "GET",
                params: new URLSearchParams(`${
                    (document ? ("?document=" + document) : "") +
                    (antecedents ? ((document ? "&" : "?") + "antecedents=" + antecedents.toString().replaceAll(",", "&antecedents=")) : "")
                }`)
            }).then((resp) => {
                this.setState((state) => {
                    state.consult.data = resp.data;
                    state.consult.isLoading = false;
                    return state;
                });
            }).catch((err) => {
                this.setState((state) => {
                    state.consult.isLoading = false;
                    return state;
                });

                if (err.status === 422) {
                    this.setState((state) => {
                        state.form.error = err.data.errors.query;
                        return state;
                    });
                } else {
                    const message = (err.status === 404) ? err.data.message : "No se pudo obtener la información de los antecedentes";
                    const title = (err.status === 404) ? "USUARIO NO ENCONTRADO" : "FALLO";

                    if (err.status === 404) {
                        err.data.message =  err.data.status
                    }
                    
                    messageError(err, message, title);
                }
            });
        }
    }

    handleChange(event, actionMeta) {
        const name = actionMeta ? actionMeta.name : event.target.name;
        const value = event.target ? event.target.value : Array.from(event, opt => opt.id);
        this.setState(state => { state.form.data[name] = value; });
    }

    handleBlur(event) {
        const elem = (event.target.id === "antecedents") ? event.target.closest("div.basic-multi-select").querySelectorAll("[name=antecedents]") : event.target;
        const name = elem.length ? elem[0].name : elem.name;
        const value = elem.length ? Array.from(elem, opt => opt.value) : elem.value;
        this.validations(name, value);
    }

    validations(name, value) {
        let message = null;

        if (name === "antecedents") {
            message = antecedentsFieldValidator(value);
        } else if (name === "document") {
            message = documentFieldValidator(value);
        }

        this.setState(state => {
            state.form.error[name] = message;
            return state;
        });
    }

    showModal(title, link) {
        this.setState(state => {
            state.modal.title = title;
            state.modal.link = link;
            return state;
        });
    }

    hideModal(event) {
        this.setState(state => {
            state.modal.title = "";
            state.modal.link = "";
            return state;
        });
    }

    render() {
        const { select, consult, form, modal } = this.state;
        return (
            <>
                <div className="page_header pb-2 mt-4 mb-2">
                    <h1>Consultar los Antecedentes de un Candidato</h1>
                    <hr className="bg-primary hr_title" />
                </div>
                <div className="row">
                    <div className="col-xl-4">
                        <Panel>
                            <PanelHeader collapse>
                                Opciones de consulta
                            </PanelHeader>
                            <PanelBody>
                                <form onSubmit={this.handleSubmit} autoComplete="off">
                                    <div className="mb-3">
                                        <label className="form-label col-form-label" htmlFor="antecedents"><b>Antecedentes</b></label>
                                        <div className="col">
                                            <Select
                                                inputId="antecedents"
                                                name="antecedents"
                                                className={"basic-multi-select" + (form.error.antecedents !== undefined ? (form.error.antecedents !== null ? " is-invalid" : " is-valid") : "")}
                                                classNamePrefix="select"
                                                placeholder="Seleccione uno o más antecedentes"
                                                maxMenuHeight={110}
                                                getOptionLabel={option => option.name}
                                                getOptionValue={option => option.id}
                                                options={select.data}
                                                onChange={this.handleChange}
                                                onBlur={this.handleBlur}
                                                isMulti
                                            />
                                            <div className="invalid-feedback">
                                                {form.error.antecedents ?? ""}
                                            </div>
                                        </div>
                                    </div>
                                    <div className="mb-3">
                                        <label className="form-label col-form-label" htmlFor="document">
                                            <b>Número de identificación del candidato</b>
                                        </label>
                                        <div className="col">
                                            <input
                                                type="text"
                                                id="document"
                                                name="document"
                                                className={"form-control" + (form.error.document !== undefined ? (form.error.document !== null ? " is-invalid" : " is-valid") : "")}
                                                placeholder="Número de identificación"
                                                onChange={this.handleChange}
                                                onBlur={this.handleBlur}
                                            />
                                            <div className="invalid-feedback">
                                                {form.error.document ?? ""}
                                            </div>
                                        </div>
                                    </div>
                                    <div className="row justify-content-end px-2">
                                        <button type="submit" className="btn btn-primary w-100px me-5px" disabled={consult.isLoading}>Consultar</button>
                                    </div>
                                </form>
                            </PanelBody>
                        </Panel>
                    </div>
                    <div className="col-xl-8">
                        <Panel>
                            <PanelHeader expand collapse>
                                Resultado de los antecedentes seleccionados
                            </PanelHeader>
                            <PanelBody>
                                {(consult.isLoading)
                                    ? <div className="row justify-content-center">
                                        <div className="spinner-border text-primary m-5" style={{ "width": "15rem", "height": "15rem" }} role="status" aria-hidden="true"></div>
                                        <span className="visually-hidden">Consultando los antecedentes...</span>
                                        <p className="text-center" style={{ whiteSpace: "pre-wrap", fontSize: "15px" }}>Este proceso puede tardar unos minutos ...</p>
                                    </div>
                                    : <></>
                                }
                                {(consult.data.length)
                                    ? <div className="card border-1">
                                        <div className="card-header">
                                            <ul className="nav nav-pills mb-2" role="tablist">
                                                {consult.data.map((elem, index) =>
                                                    <li key={"#nav-antecents-tab-" + index} className="nav-item" role="presentation">
                                                        <a href={"#nav-antecents-tab-" + index}
                                                            data-bs-toggle="tab" className={"nav-link" + (index === 0 ? " active" : "")}
                                                            aria-selected={(index === 0 ? "true" : "false")}
                                                            tabIndex={(index === 0 ? "" : "-1")}
                                                            role="tab"
                                                        >
                                                            <span className="d-sm-none">{elem.name}</span>
                                                            <span className="d-sm-block d-none">{elem.name}</span>
                                                        </a>
                                                    </li>
                                                )}
                                            </ul>
                                        </div>
                                        <div className="card-body">
                                            <div className="tab-content">
                                                {consult.data.map((elem, index) =>
                                                    <div key={"nav-antecents-tab-" + index}
                                                        className={"tab-pane fade" + (index === 0 ? " active show" : "")}
                                                        id={"nav-antecents-tab-" + index}
                                                        role="tabpanel"
                                                    >
                                                        <h3 className="mt-10px">{"Antecedente " + elem.name}</h3>
                                                        {(elem.information.title) ? <h6>{elem.information.title}</h6> : <></>}
                                                        {(elem.information.date) ? <><div>{elem.information.date}</div><br /></> : <></>}
                                                        <p style={{ textAlign: "justify" }}>{elem.information.message}</p>
                                                        {(elem.information.data) ? <p style={{ whiteSpace: "pre-wrap" }}>{elem.information.data}</p> : <></>}
                                                        {(elem.type === "no web" && elem.information.link)
                                                            ? <div className="d-grid gap-2 d-md-flex justify-content-md-end">
                                                                <button
                                                                    type="button"
                                                                    data-bs-toggle="modal"
                                                                    data-bs-target="#modalViewPDF"
                                                                    className="btn btn-success p-2"
                                                                    onClick={() => this.showModal(elem.name, elem.information.link)}
                                                                >
                                                                    <i className="fas fa-file-pdf fa-2xl"></i>
                                                                </button>
                                                            </div>
                                                            : <></>
                                                        }
                                                    </div>
                                                )}
                                            </div>
                                        </div>
                                    </div>
                                    : <></>
                                }
                            </PanelBody>
                        </Panel>
                    </div>
                   <div id="modalViewPDF" className="modal fade">
                        <div className="modal-dialog">
                            <div className="modal-content">
                                <div className="modal-header bg-dark">
                                    <h4 className="modal-title text-white">{modal.title}</h4>
                                    <button type="button" className="btn-close btn-close-white" data-bs-dismiss="modal" aria-hidden="true"></button>
                                </div>
                                <div className="modal-body p-1">
                                    {(modal.link) ? <ViewPDF endpoint={modal.link} /> : <></>}
                                </div>
                                <div className="modal-footer">
                                    <button id="close-modal" type="button" className="btn btn-primary" data-bs-dismiss="modal" aria-hidden="true">Cerrar</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </>
        );
    }
};