from typing import List, Dict, Any
import glob
import re
import json
import logging
import pdfplumber
import os

logger = logging.getLogger(__name__)


class Processing:
    """
    Class in charge of appplyig pre-processing logic to the data based on
    the content of the files
    """

    def __init__(
        self, path: str = "./data/reglamentacion/", output: str = "./data/staging/"
    ):
        self.path:str = path
        self.output:str = output
        self.hooks:List = []

    def load_pdfs(self):
        """
        Load pdfs from the path
        """
        pdfs:List[str] = glob.glob(self.path + "/*.pdf")
        logger.info(f"Se encontraron {len(pdfs)} pdfs en la ruta {self.path}")

        return pdfs

    def not_within_bboxes(self, obj, bboxes):
        """Check if the object is in any of the table's bbox."""

        def obj_in_bbox(_bbox):
            v_mid = (obj["top"] + obj["bottom"]) / 2
            h_mid = (obj["x0"] + obj["x1"]) / 2
            x0, top, x1, bottom = _bbox
            return (
                (h_mid >= x0) and (h_mid < x1) and (v_mid >= top) and (v_mid < bottom)
            )

        return not any(obj_in_bbox(__bbox) for __bbox in bboxes)

    def process_table(self, table):
        """Convert a table (list of lists) into a single string."""
        return "\n".join([" ".join(map(str, row)) for row in table])

    def pdf_to_json(self):
        """Extract text and tables from a set of PDFs."""

        pdf_files = self.load_pdfs()
        extracted_data = []

        for pdf_path in pdf_files:
            pdf_data = {
                "file_name": os.path.basename(pdf_path),
                "text": "",
                "tables": [],
            }

            with pdfplumber.open(pdf_path) as pdf:
                full_text = []
                processed_tables = []
                for page in pdf.pages:
                    # Extract tables
                    tables = page.extract_tables()
                    processed_tables.extend(
                        [self.process_table(table) for table in tables]
                    )

                    # Get text outside tables
                    bboxes = [
                        table.bbox for table in page.find_tables()
                    ]  # Find table bounding boxes
                    page_text = page.filter(
                        lambda obj: self.not_within_bboxes(obj, bboxes)
                    ).extract_text()
                    if page_text:
                        full_text.append(page_text)

                pdf_data["text"] = "\n".join(full_text)
                pdf_data["tables"] = processed_tables

            extracted_data.append(pdf_data)
            json_path = os.path.join(
                self.output, os.path.basename(pdf_path).split(".pdf")[0] + "_pre.json"
            )
            with open(json_path, "w", encoding="utf-8") as file:
                logger.info(f"Guardando los datos en el archivo {json_path}")
                json.dump(extracted_data, file, ensure_ascii=False)
