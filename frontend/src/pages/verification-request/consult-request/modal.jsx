import React from "react";
import Select from "react-select";
import ViewPDF from "./../../../components/pdf/view-pdf.jsx";
import { ConsultContext } from "./context.js";

export default class Modal extends React.Component {
    static contextType = ConsultContext;

    render() {
        const { select, handleSubmit, handleChange, handleBlur } = this.context;
        const { idModal, title, data, error, isLoading } = this.context.modal;
        return (
            <div id="modalData" className="modal fade">
                <div className="modal-dialog">
                    <div className="modal-content">
                        <div className="modal-header bg-dark">
                            <h4 className="modal-title text-white">{title}</h4>
                            <button type="button" className="btn-close btn-close-white" data-bs-dismiss="modal" aria-hidden="true"></button>
                        </div>
                        <div className={"modal-body" + (idModal === "modalViewPDF" ? " p-1" : "")}>
                            {(idModal === "modalViewPDF")
                                ? <ViewPDF endpoint={data.enpoint} />
                                : (idModal === "modalEditData")
                                    ? <form autoComplete="off">
                                        <div className="mb-3">
                                            <label className="form-label" htmlFor="title"><b>Título</b></label>
                                            <input
                                                id="title"
                                                name="title"
                                                type="text"
                                                placeholder="Título"
                                                defaultValue={data.title}
                                                className={"form-control" + (error.title !== undefined ? (error.title !== null ? " is-invalid" : " is-valid") : "")}
                                                onChange={(e) => handleChange(e, undefined, "modal")}
                                                onBlur={(e) => handleBlur(e, "modal")}
                                            />
                                            <div className="invalid-feedback">
                                                {error.title ?? ""}
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
                                                    defaultValue={data.document}
                                                    className={"form-control" + (error.document !== undefined ? (error.document !== null ? " is-invalid" : " is-valid") : "")}
                                                    onChange={(e) => handleChange(e, undefined, "modal")}
                                                    onBlur={(e) => handleBlur(e, "modal")}
                                                />
                                                <div className="invalid-feedback">
                                                    {error.document ?? ""}
                                                </div>
                                            </div>
                                        </div>
                                    </form>
                                    : (idModal === "modalEditState")
                                        ? <form autoComplete="off">
                                            <div className="mb-3">
                                                <label className="form-label col-form-label" htmlFor="edit-state"><b>Estado</b></label>
                                                <div className="col">
                                                    <Select
                                                        inputId="edit-state"
                                                        name="state"
                                                        placeholder="Seleccione un tipo de antecedente"
                                                        defaultValue={select.dataEdit.filter(opt => opt.value === data.state)}
                                                        className={"basic-single" + (error.state !== undefined ? (error.state !== null ? " is-invalid" : " is-valid") : "")}
                                                        classNamePrefix="select"
                                                        maxMenuHeight={110}
                                                        options={select.dataEdit}
                                                        onChange={(value, actionMeta) => handleChange(value, actionMeta, "modal")}
                                                        onBlur={(e) => handleBlur(e, "modal")}
                                                    />
                                                    <div className="invalid-feedback">
                                                        {error.state ?? ""}
                                                    </div>
                                                </div>
                                            </div>
                                            <div className="mb-3">
                                                <label className="form-label col-form-label" htmlFor="comment"><b>Comentario</b></label>
                                                <div className="col">
                                                    <textarea
                                                        id="comment"
                                                        name="comment"
                                                        placeholder="Comentario"
                                                        defaultValue={data.comment}
                                                        className={"form-control" + (error.comment !== undefined ? (error.comment !== null ? " is-invalid" : " is-valid") : "")}
                                                        rows="3"
                                                        onChange={(e) => handleChange(e, undefined, "modal")}
                                                        onBlur={(e) => handleBlur(e, "modal")}
                                                    ></textarea>
                                                    <div className="invalid-feedback">
                                                        {error.comment ?? ""}
                                                    </div>
                                                </div>
                                            </div>
                                        </form>
                                        : (idModal === "modalEditDoc")
                                            ? <form autoComplete="off">
                                                <div className="mb-3">
                                                    <label className="form-label col-form-label" htmlFor="file_document">Documento</label>
                                                    <div className="col">
                                                        <input
                                                            id="file_document"
                                                            name="file_document"
                                                            type="file"
                                                            className={"form-control" + (error.file_document !== undefined ? (error.file_document !== null ? " is-invalid" : " is-valid") : "")}
                                                            accept=".pdf"
                                                            onChange={(e) => handleChange(e, undefined, "modal")}
                                                            onBlur={(e) => handleBlur(e, "modal")}
                                                        />
                                                        <div className="invalid-feedback">
                                                            {error.file_document ?? ""}
                                                        </div>
                                                    </div>
                                                </div>
                                            </form>
                                            : <></>
                            }
                        </div>
                        <div className="modal-footer">
                            <button id="close-modal" type="button" className="btn btn-primary" data-bs-dismiss="modal" aria-hidden="true">Cerrar</button>
                            {(idModal !== "modalViewPDF")
                                ? <button className="btn btn-success" type="button" onClick={handleSubmit} disabled={isLoading}>
                                    {(isLoading) ? <><span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>&nbsp;</> : <></>}
                                    Actualizar
                                </button>
                                : <></>
                            }
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}