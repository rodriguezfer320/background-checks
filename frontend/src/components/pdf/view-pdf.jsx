import React from "react";
import { CharacterMap, Viewer } from "@react-pdf-viewer/core";
import pdfjsWorker from "pdfjs-dist/build/pdf.worker.entry";
import { ApiBaseRoute } from "./../../composables/config.js";

const characterMap: CharacterMap = {
    isCompressed: true,
    url: pdfjsWorker,
};

export default class ViewPDF extends React.Component {
    render() {
        return (
            <div style={{ height: "500px" }}>
                <div style={{ overflow: "auto", border: "1px solid rgba(0, 0, 0, 0.3)", height: "100%" }}>
                    <Viewer characterMap={characterMap} fileUrl={ApiBaseRoute + this.props.endpoint} />
                </div>
            </div>
        );
    }
};