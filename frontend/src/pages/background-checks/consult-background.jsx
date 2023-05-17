import React, { Component } from "react";
import Select from "react-select";
import Swal from "sweetalert2";
import { Panel, PanelHeader, PanelBody } from "../../components/panel/panel.jsx";
import ViewPDF from "../../components/pdf/view-pdf.jsx";
import { fetchData } from "../../composables/api.js";
import { documentFieldValidator, antecedentsFieldValidator } from "../../composables/validators.js";
import { ApiBaseRoute } from "../../composables/config.js";

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
    }

    componentDidMount() {
        this.setState(state => {
            state.select.isLoading = true;
            return state;
        });

        setTimeout(() => {
            fetchData({
                endpoint: "/api/antecedentes",
                signal: this.abortController.signal,
                method: "GET"
            }).then((res) => {
                this.setState((state) => {
                    state.select.data = res.data;
                    return state;
                });
            }).catch((err) => {
                Swal.fire({
                    title: "Fallo",
                    text: "Ocurrio un error inesperado: " + err.message,
                    icon: "error",
                    confirmButtonText: "OK",
                    confirmButtonColor: "#2d353c"
                });
                console.error(err);
            }).finally(
                this.setState(state => {
                    state.select.isLoading = false;
                    return state;
                })
            );
        }, 500);

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

            setTimeout(() => {
                fetchData({
                    endpoint: "/api/verificacion-antecedentes",
                    signal: this.abortController.signal,
                    method: "GET",
                    params: new URLSearchParams(`${
                        (document ? ("?document=" + document) : "") +
                        (antecedents ? ((document ? "&" : "?") + "antecedents=" + antecedents.toString().replaceAll(",", "&antecedents=")) : "")
                    }`)
                }).then((res) => {
                    this.setState((state) => {
                        state.consult.data = res.data;
                        return state;
                    });
                }).catch((err) => {
                    if (err.response.status === 422) {
                        this.setState((state) => {
                            state.form.error = err.response.data.errors.query;
                            return state;
                        });
                    } else {
                        Swal.fire({
                            title: "Fallo",
                            text: "Ocurrio un error inesperado: " + err.message,
                            icon: "error",
                            confirmButtonText: "OK",
                            confirmButtonColor: "#2d353c"
                        });
                        console.error(err);
                    }
                }).finally(
                    this.setState(state => {
                        state.consult.isLoading = false;
                        return state;
                    })
                );
            }, 500);
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
                                    </div>
                                    : <></>
                                }
                                {(consult.data.length)
                                    ? <div className="card border-1">
                                        <div className="card-header">
                                            <ul className="nav nav-pills card-header-pills mb-2" role="tablist">
                                                {consult.data.map((elem, index) =>
                                                    <li key={"#nav-antecents-tab-" + index} className="nav-item" role="presentation">
                                                        <a href={"#nav-antecents-tab-" + index}
                                                            data-bs-toggle="tab" className={"nav-link" + (index === 0 ? " active" : "")}
                                                            aria-selected={(index === 0 ? "true" : "false")}
                                                            tabIndex={(index === 0 ? "" : "-1")}
                                                            role="tab"
                                                        >
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
                                                        {(elem.information.data) ? <div><pre>{elem.information.data}</pre></div> : <></>}
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
                    {(consult.data.length && consult.data.find((elem) => elem.type === "no web"))
                        ? <div id="modalViewPDF" className="modal fade">
                            <div className="modal-dialog">
                                <div className="modal-content">
                                    <div className="modal-header bg-dark">
                                        <h4 className="modal-title text-white">{modal.title}</h4>
                                        <button type="button" className="btn-close btn-close-white" data-bs-dismiss="modal" aria-hidden="true"></button>
                                    </div>
                                    <div className="modal-body p-1">
                                        <ViewPDF fileUrl={ApiBaseRoute + modal.link} />
                                    </div>
                                    <div className="modal-footer">
                                        <button id="close-modal" type="button" className="btn btn-primary" data-bs-dismiss="modal" aria-hidden="true">Cerrar</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        : <></>
                    }
                </div>
            </>
        );
    }
};