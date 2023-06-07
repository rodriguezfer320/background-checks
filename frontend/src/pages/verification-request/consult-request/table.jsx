import React from "react";
import { Panel, PanelHeader, PanelBody, PanelFooter } from "./../../../components/panel/panel.jsx";
import { ConsultContext } from "./context.js";
import { Roles } from "./../../../composables/config.js";
import { getUserRole } from "./../../../composables/sessionData.js";

export default class Table extends React.Component {
    static contextType = ConsultContext;

    render() {
        const { showModal, consultDataTable } = this.context;
        const { pagination, dataRes } = this.context.consult;
        return (
            <div className="col-xl-8">
                <Panel>
                    <PanelHeader expand collapse>
                        Solicitudes de verificación
                    </PanelHeader>
                    <PanelBody>
                        <div className="py-1">
                            <small><strong>Mostrando registros del {pagination.first | 0} al {pagination.last | 0} de un total de {pagination.total | 0} registro(s).</strong></small>
                        </div>
                        <div className="table-responsive">
                            <table className="table table-striped table-bordered table-hover">
                                <thead className="align-middle text-center bg-secondary text-white">
                                    <tr>
                                        <th width="1%">Id</th>
                                        <th width="3%" hidden={getUserRole() === Roles.candidate}>Número de identificación</th>
                                        <th>Título</th>
                                        <th>Comentario</th>
                                        <th width="2%">Estado</th>
                                        <th width="1%">Acciones</th>
                                    </tr>
                                </thead>
                                <tbody className="align-middle">
                                    {(dataRes.length)
                                        ? dataRes.map((item, index) =>
                                            <tr key={"data-verification-request-" + index}>
                                                <td className="text-center">{item.id}</td>
                                                <td id={"document-" + item.id} hidden={getUserRole() === Roles.candidate} className="text-center">{item.candidate_id}</td>
                                                <td id={"title-" + item.id}>{item.title}</td>
                                                <td id={"comment-" + item.id}>{item.comment}</td>
                                                <td id={"state-" + item.id}>{item.state}</td>
                                                <td nowrap="true">
                                                    <button
                                                        type="button"
                                                        id="modalViewPDF"
                                                        data-bs-toggle="modal"
                                                        data-bs-target="#modalData"
                                                        className="btn btn-success me-1 p-1"
                                                        onClick={showModal}
                                                    >
                                                        <i className="fas fa-file-pdf fa-xl"></i>
                                                    </button>
                                                    {(getUserRole() === Roles.candidate)
                                                        ? <button
                                                            type="button"
                                                            id="modalEditData"
                                                            data-bs-toggle="modal"
                                                            data-bs-target="#modalData"
                                                            className="btn btn-primary me-1 p-1"
                                                            onClick={showModal}
                                                        >
                                                            <i className="fas fa-pen-to-square fa-xl"></i>
                                                        </button>
                                                        : <></>
                                                    }
                                                    {(getUserRole() !== Roles.candidate)
                                                        ? <button
                                                            type="button"
                                                            id="modalEditState"
                                                            data-bs-toggle="modal"
                                                            data-bs-target="#modalData"
                                                            className="btn btn-primary me-1 p-1"
                                                            onClick={showModal}
                                                        >
                                                            <i className="fas fa-pen-to-square fa-xl"></i>
                                                        </button>
                                                        : <></>
                                                    }
                                                    {(getUserRole() === Roles.candidate && item.state === "rechazada")
                                                        ? <button
                                                            type="button"
                                                            id="modalEditDoc"
                                                            data-bs-toggle="modal"
                                                            data-bs-target="#modalData"
                                                            className="btn btn-warning p-1"
                                                            onClick={showModal}
                                                        >
                                                            <i className="fas fa-file-pen fa-xl"></i>
                                                        </button>
                                                        : <></>
                                                    }
                                                </td>
                                            </tr>
                                        )
                                        : <tr>
                                            <td colSpan={6} className="text-center h-100px">
                                                No se encontraron resultados para la consulta realizada
                                            </td>
                                        </tr>
                                    }
                                </tbody>
                            </table>
                        </div>
                    </PanelBody>
                    <PanelFooter>
                        {(dataRes.length)
                            ? <div className="pagination pagination-sm justify-content-center">
                                <div className={"page-item" + (pagination.prev_page ? "" : " disabled")}>
                                    <a href="/" className="page-link" onClick={(e) => consultDataTable(e, pagination.prev_page)}>«</a>
                                </div>
                                {pagination.pages.map((page, index) =>
                                    <div key={"page-item-" + index} className={"page-item" + (pagination.current_page === page ? " active" : "")}>
                                        {(page)
                                            ? <a href="/" className="page-link" onClick={(e) => consultDataTable(e, (pagination.current_page === page ? null : page))}>{page}</a>
                                            : <div style={{ padding: "4px 0px", margin: "0px 0px 0px 6px" }}>...</div>
                                        }
                                    </div>
                                )}
                                <div className={"page-item" + (pagination.next_page ? "" : " disabled")}>
                                    <a href="/" className="page-link" onClick={(e) => consultDataTable(e, pagination.next_page)}>»</a>
                                </div>
                            </div>
                            : <></>
                        }
                    </PanelFooter>
                </Panel>
            </div>
        );
    }
}