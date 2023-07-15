import React from "react";
import Select from "react-select";
import { Panel, PanelHeader, PanelBody, PanelFooter } from "./../../components/panel/panel.jsx";
import { fetchData } from "./../../composables/backgroundCheckApi.js";
import {
    titleFieldValidator, documentFieldValidator,
    antecedentFieldValidator, documentFileFieldValidator
} from "./../../composables/validators.js";
import { getUserSubKey } from "./../../composables/sessionData.js";
import { messageError, messageSuccess } from "./../../composables/alert.js";

export default class CreateRequest extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            select: {
                data: [],
                isLoading: false
            },
            form: {
                data: {
                    user_sub_key: getUserSubKey()
                },
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

        fetchData({
            endpoint: "/antecedentes?type=no web",
            signal: this.abortController.signal,
            method: "GET"
        }).then((resp) => {
            this.setState(state => {
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

            Object.keys(data).forEach((key) => {
                dataTemp.append(key, data[key]);
            });

            this.setState(state => {
                state.form.isLoading = true;
                return state;
            });

            fetchData({
                endpoint: "/verificacion-solicitud/crear",
                signal: this.abortController.signal,
                method: "POST",
                data: dataTemp
            }).then((resp) => {
                this.setState(state => {
                    state.form.data = {
                        user_sub_key: state.form.data.user_sub_key
                    };
                    state.form.error = {};
                    state.form.isLoading = false;
                    return state;
                });
                event.target.reset();
                messageSuccess(resp.data.status, resp.data.message);
            }).catch((err) => {
                this.setState(state => {
                    state.form.isLoading = false;
                    return state;
                });

                if (err.status === 422) {
                    this.setState(state => {
                        state.form.error = err.data.errors.form;
                        return state;
                    });
                } else {
                    const message = (err.data && err.data.status === "FAILD") ? err.data.message : "No se pudo crear la solicitud de verificación";
                    messageError(err, message);
                }
            });
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
                                    <button className="btn btn-success w-100px me-5px" type="submit" disabled={form.isLoading}>
                                        {(form.isLoading) ? <><span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;</> : <></>}
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