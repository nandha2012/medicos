import os
from docx import Document
from utils.dates import generate_dir_name

# nas_main.py sets OUTPUT_DIR=output/nas before importing this module,
# so we just use OUTPUT_DIR directly — no extra "nas" suffix needed.
NAS_BASE_OUTPUT_DIR = os.getenv("OUTPUT_DIR") or "output"


class NASTemplateService:
    """
    Fills NAS fax transmittal templates (NAS_MR_MOTHER.docx / NAS_MR_INFANT.docx)
    by locating known label cells in tables and writing values into the adjacent
    blank cells. No #{placeholder}# markers are added to the templates.
    """

    # Maps lowercased label text (stripped of trailing ':') → data dict key.
    # Mother and infant labels are distinct so a single mapping covers both templates.
    LABEL_TO_FIELD = {
        "mother's last name":   "mothr_last_name",
        "mother's first name":  "mothr_first_name",
        "mother's dob":         "mothr_dob",
        "medical record #":     "chart4",
        "facility":             "hos_name",
        "date of delivery/service": "dob",
        # Infant template labels
        "child's last name":    "lastname_infant",
        "child's first name":   "firstname_infant",
        "child's dob":          "dob",
    }

    def __init__(self):
        # output/nas/<date>/
        self.output_dir = os.path.join(NAS_BASE_OUTPUT_DIR, generate_dir_name())
        os.makedirs(self.output_dir, exist_ok=True)

    def _normalize_label(self, text: str) -> str:
        """Strip whitespace and trailing colon, lowercase, normalise curly quotes."""
        normalized = text.strip().lower().rstrip(':').strip()
        # Word templates often use curly apostrophes (U+2018/U+2019); normalise to straight
        normalized = normalized.replace('\u2018', "'").replace('\u2019', "'")
        return normalized

    def _set_cell_value(self, cell, value: str):
        """
        Write value into the first paragraph of a cell while preserving
        the existing paragraph/run formatting.
        """
        if not cell.paragraphs:
            return
        para = cell.paragraphs[0]
        # Clear all runs
        for run in para.runs:
            run.text = ''
        if para.runs:
            para.runs[0].text = value
        else:
            para.add_run(value)

    def _fill_table_cells(self, doc, data: dict):
        """
        Iterate every table row. For each cell whose normalised text matches
        a known label, fill the next cell in the same row with the mapped value.
        Skips the fill if the value is empty/None or the cells are merged
        (same object reference).
        """
        for table in doc.tables:
            for row in table.rows:
                cells = row.cells
                for i, cell in enumerate(cells):
                    label = self._normalize_label(cell.text)
                    if label not in self.LABEL_TO_FIELD:
                        continue
                    if i + 1 >= len(cells):
                        continue
                    next_cell = cells[i + 1]
                    # Skip merged cells (python-docx returns same object)
                    if next_cell is cell:
                        continue
                    field = self.LABEL_TO_FIELD[label]
                    raw = data.get(field, "")
                    value = str(raw) if raw not in ("", None) else ""
                    if value:
                        self._set_cell_value(next_cell, value)

    def fill_template(self, template_path: str, data: dict,
                      sub_dir: str, output_filename: str) -> str:
        """
        Open template_path, fill table cells from data, save filled docx.

        Args:
            template_path:   Absolute path to the .docx template.
            data:            Flat dict of field values.
            sub_dir:         Sub-directory under the dated output folder.
            output_filename: File name (without extension) for the saved docx.

        Returns:
            Absolute path to the saved .docx file.
        """
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"NAS template not found: {template_path}")

        doc = Document(template_path)
        self._fill_table_cells(doc, data)

        dest_dir = os.path.join(self.output_dir, sub_dir)
        os.makedirs(dest_dir, exist_ok=True)

        out_path = os.path.join(dest_dir, f"{output_filename}.docx")
        doc.save(out_path)
        print(f"📄 Saved filled docx: {out_path}")
        return out_path
