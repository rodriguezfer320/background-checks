import React from "react";
import Select from "react-select";
import { Panel, PanelHeader, PanelBody } from "./../../../components/panel/panel.jsx";
import { ConsultContext } from "./context.js";
import { Roles } from "./../../../composables/config.js";
import { getUserRole } from "./../../../composables/sessionData.js";

export default class Table extends React.Component {
    static contextType = ConsultContext;

    render() {
        const { select, consult, consultDataTable, handleChange, handleBlur } = this.context;
        return (
            <div className="col-xl-4">
                <Panel>
                    <PanelHeader collapse>
                        Opciones de consulta
                    </PanelHeader>
                    <PanelBody>
                        <form onSubmit={(e) => consultDataTable(e, 1)} autoComplete="off">
                            <div className="mb-3">
                                <label className="form-label col-form-label" htmlFor="consult-state"><b>Estado</b></label>
                                <div className="col">
                                    <Select
                                        inputId="consult-state"
                                        name="state"
                                        defaultValue={select.dataForm[0]}
                                        className="basic-single"
                                        classNamePrefix="select"
                                        placeholder="Seleccione un estado"
                                        maxMenuHeight={110}
                                        options={select.dataForm}
                                        onChange={(value, actionMeta) => handleChange(value, actionMeta, "consult")}
                                    />
                                </div>
                            </div>
                            <div className="mb-3">
                                <label className="form-label col-form-label" htmlFor="search">
                                    <b>Buscar</b>
                                </label>
                                <div className="col">
                                    <input
                                        type="text"
                                        id="search"
                                        name="search"
                                        className={"form-control" + (consult.error.search !== undefined ? (consult.error.search !== null ? " is-invalid" : " is-valid") : "")}
                                        placeholder={"Id solicitud" + (getUserRole() !== Roles.candidate ? ", Número de identificación" : "")}
                                        onChange={(e) => handleChange(e, undefined, "consult")}
                                        onBlur={(e) => handleBlur(e, "consult")}
                                    />
                                    <div className="invalid-feedback">
                                        {consult.error.search ?? ""}
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
        );
    }
}