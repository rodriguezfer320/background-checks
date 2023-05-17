import React from "react";
import { Worker, Viewer } from "@react-pdf-viewer/core";

export default class ViewPDF extends React.Component {
    render() {
        return (
            <div style={{ height: "500px" }}>
                <div style={{ overflow: "auto", border: "1px solid rgba(0, 0, 0, 0.3)", height: "100%" }}>
                    <Worker workerUrl="https://unpkg.com/pdfjs-dist@3.5.141/build/pdf.worker.min.js">
                        <Viewer fileUrl={this.props.fileUrl} />
                    </Worker>
                </div>
            </div>
        );
    }

};