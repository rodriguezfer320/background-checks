import React from "react";
import { Viewer } from "@react-pdf-viewer/core";
import pdfjsWorker from "pdfjs-dist/build/pdf.worker.entry";
import { fetchData } from "./../../composables/backgroundCheckApi.js";

//css
import '@react-pdf-viewer/core/lib/styles/index.css';

export default class ViewPDF extends React.Component {
    constructor(props) {
		super(props);
		this.state = {
			file: null,
			error: null,
            characterMap: {
                isCompressed: true,
                url: pdfjsWorker
            }
		};
	}

    componentDidMount() {
        fetchData({
            endpoint: this.props.endpoint,
            method: "GET",
            responseType: "arraybuffer"
        }).then(resp => {
            this.setState(state => {
                state.file = [...new Uint8Array(resp.data)];
                return state;
            });
        }).catch(err => {
            this.setState(state => {
                state.error = "No se puedo cargar el documento, debido aún fallo inesperado. Estado: " + err.status;
                return state;
            });
        });
    }

    render() {
        return (
            <div style={{ height: "500px" }}>
                <div style={{ overflow: "auto", border: "1px solid rgba(0, 0, 0, 0.3)", height: "100%" }}>
                    {(this.state.file)
                        ? <Viewer characterMap={this.state.characterMap} fileUrl={this.state.file} />
                        : (this.state.error)
                            ? <div className="rpv-core__doc-error">
                                <div className="rpv-core__doc-error-text">{this.state.error}</div>
                              </div>
                            : <></>
                    }
                </div>
            </div>
        );
    }
};