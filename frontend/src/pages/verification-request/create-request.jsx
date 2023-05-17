import React from "react";
import Select from "react-select";
import Swal from "sweetalert2";
import { Panel, PanelHeader, PanelBody, PanelFooter } from "../../components/panel/panel.jsx";
import { fetchData } from "../../composables/api.js";
import {
    titleFieldValidator, documentFieldValidator,
    antecedentFieldValidator, documentFileFieldValidator
} from "../../composables/validators.js";

export default class CreateRequest extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            select: {
                data: [],
                isLoading: false
            },
            form: {
                data: {},
                error: {},
                isLoading: false
            }
        };

        this.abortController = new AbortController();
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.handleBlur = this.handleBlur.bind(this);
    }

    componentDidMount() {
        this.setState(state => {
            state.select.isLoading = true;
            return state;
        });

        setTimeout(() => {
            fetchData({
                endpoint: "/api/antecedentes?type=no web",
                signal: this.abortController.signal,
                method: "GET"
            }).then((res) => {
                this.setState(state => {
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
        if (this.state.select.isLoading) {
            this.abortController.abort();
        }
    }

    handleSubmit(event) {
        event.preventDefault();
        const errors = [
            this.state.form.error.title,
            this.state.form.error.document,
            this.state.form.error.antecedent,
            this.state.form.error.file_document
        ];
        const data = this.state.form.data;

        if (errors.includes(undefined)) {
            const keys = ["title", "document", "antecedent", "file_document"];

            errors.forEach((elem, index) => {
                if (elem === undefined) {
                    this.validations(keys[index], data[keys[index]]);
                }
            });
        } else if (!errors.some((v) => v !== null)) {
            const dataTemp = new FormData();

            if (data["file_document"]) {
                dataTemp.append("file_document_copy", data["file_document"]);
            }

            Object.keys(data).forEach((key) => {
                dataTemp.append(key, data[key]);
            });

            this.setState(state => {
                state.form.isLoading = true;
                return state;
            });

            setTimeout(() => {
                fetchData({
                    endpoint: "/api/verificacion-solicitud/crear",
                    signal: this.abortController.signal,
                    method: "POST",
                    data: dataTemp
                }).then((res) => {
                    this.setState(state => {
                        state.form.data = {};
                        state.form.error = {};
                        return state;
                    });
                    event.target.reset();
                    Swal.fire({
                        title: res.status,
                        text: res.message,
                        icon: "success",
                        confirmButtonText: "OK",
                        confirmButtonColor: "#2d353c"
                    })
                }).catch((err) => {
                    if (err.response.status === 422) {
                        this.setState(state => {
                            state.form.error = err.response.data.errors.form;
                            return state;
                        });
                    } else {
                        const text = (err.response.data.status === "FAILD") ? err.response.data.message : "Ocurrio un error inesperado: " + err.message;
                        Swal.fire({
                            title: "Fallo",
                            text,
                            icon: "error",
                            confirmButtonText: "OK",
                            confirmButtonColor: "#2d353c"
                        });
                        if (err.response.data.status !== "FAILD") { console.error(err); }
                    }
                }).finally(
                    this.setState(state => {
                        state.form.isLoading = false;
                        return state;
                    })
                );
            }, 500);
        }
    }

    handleChange(event, actionMeta) {
        const name = actionMeta ? actionMeta.name : event.target.name;
        const value = event.target ? (event.target.files ? event.target.files[0] : event.target.value) : event.id;
        this.setState(state => {
            state.form.data[name] = value;
            return state;
        });
    }

    handleBlur(event) {
        const elem = (event.target.id === "antecedent") ? event.target.closest("div.basic-single").querySelector("[name=antecedent]") : event.target;
        const name = elem.name;
        const value = elem.files ? elem.files[0] : elem.value;
        this.validations(name, value);
    }

    validations(name, value) {
        let message = null;

        if (name === "title") {
            message = titleFieldValidator(value);
        } else if (name === "document") {
            message = documentFieldValidator(value);
        } else if (name === "antecedent") {
            message = antecedentFieldValidator(value);
        } else if (name === "file_document") {
            message = documentFileFieldValidator(value);
        }

        this.setState(state => {
            state.form.error[name] = message;
            return state;
        });
    }

    render() {
        const { select, form } = this.state;
        return (
            <div className="row justify-content-center">
                <div className="col-xl-5">
                    <Panel>
                        <PanelHeader className="text-center text-uppercase">
                            datos de la solicitud de verificación
                        </PanelHeader>
                        <form onSubmit={this.handleSubmit} autoComplete="off">
                            <PanelBody>
                                <div className="mb-3">
                                    <label className="form-label" htmlFor="title"><b>Título</b></label>
                                    <input
                                        id="title"
                                        name="title"
                                        type="text"
                                        placeholder="Título"
                                        className={"form-control" + (form.error.title !== undefined ? (form.error.title !== null ? " is-invalid" : " is-valid") : "")}
                                        onChange={this.handleChange}
                                        onBlur={this.handleBlur}
                                    />
                                    <div className="invalid-feedback">
                                        {form.error.title ?? ""}
                                    </div>
                                </div>
                                <div className="mb-3">
                                    <label className="form-label col-form-label" htmlFor="document"><b>Número de identificación</b></label>
                                    <div className="col">
                                        <input
                                            id="document"
                                            name="document"
                                            type="text"
                                            placeholder="Número de identificación"
                                            className={"form-control" + (form.error.document !== undefined ? (form.error.document !== null ? " is-invalid" : " is-valid") : "")}
                                            onChange={this.handleChange}
                                            onBlur={this.handleBlur}
                                        />
                                        <div className="invalid-feedback">
                                            {form.error.document ?? ""}
                                        </div>
                                    </div>
                                </div>
                                <div className="mb-3">
                                    <label className="form-label col-form-label" htmlFor="antecedent"><b>Tipo de antecedente</b></label>
                                    <div className="col">
                                        <Select
                                            inputId="antecedent"
                                            name="antecedent"
                                            value={select.data.filter(({ id }) => id === form.data.antecedent)}
                                            placeholder="Seleccione un tipo de antecedente"
                                            className={"basic-single" + (form.error.antecedent !== undefined ? (form.error.antecedent !== null ? " is-invalid" : " is-valid") : "")}
                                            classNamePrefix="select"
                                            maxMenuHeight={110}
                                            getOptionLabel={option => option.name}
                                            getOptionValue={option => option.id}
                                            options={select.data}
                                            onChange={this.handleChange}
                                            onBlur={this.handleBlur}
                                        />
                                        <div className="invalid-feedback">
                                            {form.error.antecedent ?? ""}
                                        </div>
                                    </div>
                                </div>
                                <div className="mb-3">
                                    <label className="form-label col-form-label" htmlFor="file_document">Documento</label>
                                    <div className="col">
                                        <input
                                            id="file_document"
                                            name="file_document"
                                            type="file"
                                            className={"form-control" + (form.error.file_document !== undefined ? (form.error.file_document !== null ? " is-invalid" : " is-valid") : "")}
                                            accept=".pdf"
                                            onChange={this.handleChange}
                                            onBlur={this.handleBlur}
                                        />
                                        <div className="invalid-feedback">
                                            {form.error.file_document ?? ""}
                                        </div>
                                    </div>
                                </div>
                            </PanelBody>
                            <PanelFooter>
                                <div className="row justify-content-end px-2">
                                    <button class="btn btn-success w-100px me-5px" type="submit" disabled={form.isLoading}>
                                        {(form.isLoading) ? <><span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;</> : <></>}
                                        Registrar
                                    </button>
                                </div>
                            </PanelFooter>
                        </form>
                    </Panel>
                </div>
            </div>
        );
    }
};