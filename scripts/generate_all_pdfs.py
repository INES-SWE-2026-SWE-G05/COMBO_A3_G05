import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute total pages."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#7E8881"))
        self.drawString(54, letter[1] - 36, "AgriSoko Pocket (COMBO_A3_G05) — Formal Coursework Deliverable")
        self.setStrokeColor(colors.HexColor("#D8E2DC"))
        self.setLineWidth(0.5)
        self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)
        self.line(54, 45, letter[0] - 54, 45)
        self.drawString(54, 32, "Confidential & Verified Academic Artifact — Release v1.0.0 (Commit 8f1e4a6)")
        self.drawRightString(letter[0] - 54, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def md_to_html(text: str) -> str:
    # First escape HTML special characters except existing safe tags
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # Bold **text**
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
    # Italic *text*
    text = re.sub(r"(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)", r"<i>\1</i>", text)
    # Code `code`
    text = re.sub(r"`(.*?)`", r'<font face="Courier">\1</font>', text)
    # Markdown links [text](url)
    text = re.sub(r"\[(.*?)\]\((.*?)\)", r'<font color="#1A4D2E"><u>\1</u></font>', text)
    return text


def create_pdf_from_markdown_sections(markdown_text: str, output_path: Path, doc_title: str):
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1A4D2E"),
        spaceAfter=6,
    )
    h1_style = ParagraphStyle(
        "DocH1",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#1A4D2E"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True,
    )
    h2_style = ParagraphStyle(
        "DocH2",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#2D6A4F"),
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True,
    )
    h3_style = ParagraphStyle(
        "DocH3",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#0F1E17"),
        spaceBefore=5,
        spaceAfter=2,
        keepWithNext=True,
    )
    body_style = ParagraphStyle(
        "DocBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0F1E17"),
        spaceAfter=3,
    )
    bullet_style = ParagraphStyle(
        "DocBullet",
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=2,
    )
    code_style = ParagraphStyle(
        "DocCode",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=6.8,
        leading=8.5,
        textColor=colors.HexColor("#0F1E17"),
        spaceAfter=2,
    )
    table_cell = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7,
        leading=9,
        textColor=colors.HexColor("#0F1E17"),
    )
    table_header = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7,
        leading=9,
        textColor=colors.white,
    )

    story = []
    lines = markdown_text.split("\n")
    i = 0
    in_code_block = False
    code_lines = []

    while i < len(lines):
        line = lines[i]

        if line.startswith("<!-- PAGE "):
            story.append(PageBreak())
            i += 1
            continue

        if line.startswith("```"):
            if in_code_block:
                in_code_block = False
                code_text = "<br/>".join(code_lines).replace(" ", "&nbsp;")
                story.append(Paragraph(code_text, code_style))
                story.append(Spacer(1, 4))
                code_lines = []
            else:
                in_code_block = True
                code_lines = []
            i += 1
            continue

        if in_code_block:
            safe = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            code_lines.append(safe)
            i += 1
            continue

        # Markdown Table Detection
        if "|" in line and i + 1 < len(lines) and ("| :---" in lines[i + 1] or "| ---" in lines[i + 1]):
            table_raw = []
            headers = [c.strip() for c in line.strip().strip("|").split("|")]
            table_raw.append([Paragraph(f"<b>{md_to_html(h)}</b>", table_header) for h in headers])
            i += 2  # Skip separator line
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                row_cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                formatted_cells = [Paragraph(md_to_html(cell), table_cell) for cell in row_cells]
                table_raw.append(formatted_cells)
                i += 1

            col_count = len(headers)
            avail_width = letter[0] - 108
            col_widths = [avail_width / col_count] * col_count
            if col_count == 4:
                col_widths = [avail_width * 0.18, avail_width * 0.22, avail_width * 0.35, avail_width * 0.25]
            elif col_count == 5:
                col_widths = [avail_width * 0.16, avail_width * 0.18, avail_width * 0.26, avail_width * 0.26, avail_width * 0.14]
            elif col_count == 6:
                col_widths = [avail_width * 0.18, avail_width * 0.12, avail_width * 0.16, avail_width * 0.14, avail_width * 0.20, avail_width * 0.20]
            elif col_count == 8:
                col_widths = [avail_width * 0.08, avail_width * 0.24, avail_width * 0.12, avail_width * 0.14, avail_width * 0.14, avail_width * 0.08, avail_width * 0.08, avail_width * 0.12]
            elif col_count == 10:
                col_widths = [avail_width * 0.14, avail_width * 0.09, avail_width * 0.14, avail_width * 0.11, avail_width * 0.06, avail_width * 0.14, avail_width * 0.06, avail_width * 0.11, avail_width * 0.07, avail_width * 0.08]

            t = Table(table_raw, colWidths=col_widths, repeatRows=1)
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1A4D2E")),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#FAF8F5"), colors.HexColor("#F2EDE4")]),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D8E2DC")),
            ]))
            story.append(t)
            story.append(Spacer(1, 4))
            continue

        if not line.strip():
            story.append(Spacer(1, 2))
            i += 1
            continue

        if line.startswith("# "):
            story.append(Paragraph(line[2:].strip(), title_style))
            story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1A4D2E"), spaceAfter=6))
        elif line.startswith("## "):
            story.append(Paragraph(line[3:].strip(), h1_style))
        elif line.startswith("### "):
            story.append(Paragraph(line[4:].strip(), h2_style))
        elif line.startswith("#### "):
            story.append(Paragraph(line[5:].strip(), h3_style))
        elif line.startswith("* ") or line.startswith("- "):
            raw = md_to_html(line[2:].strip())
            story.append(Paragraph(f"• &nbsp; {raw}", bullet_style))
        elif re.match(r"^\d+\.\s", line):
            raw = md_to_html(re.sub(r"^\d+\.\s", "", line).strip())
            num = line.split(".")[0].strip()
            story.append(Paragraph(f"<b>{num}.</b> &nbsp; {raw}", bullet_style))
        else:
            raw = md_to_html(line.strip())
            story.append(Paragraph(raw, body_style))

        i += 1

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated: {output_path}")


def main():
    root = Path(__file__).resolve().parents[1]
    
    # 1. TEST_LOG.pdf
    test_log_md = (root / "evidence" / "TEST_LOG.md").read_text()
    create_pdf_from_markdown_sections(test_log_md, root / "evidence" / "TEST_LOG.pdf", "Test Log & Verification")

    # 2. FEEDBACK.pdf
    feedback_md = (root / "evidence" / "FEEDBACK.md").read_text()
    create_pdf_from_markdown_sections(feedback_md, root / "evidence" / "FEEDBACK.pdf", "Stakeholder Feedback Report")

    # 3. CONTRIBUTIONS.pdf
    contributions_md = (root / "evidence" / "CONTRIBUTIONS.md").read_text()
    create_pdf_from_markdown_sections(contributions_md, root / "evidence" / "CONTRIBUTIONS.pdf", "Signed Contribution Sheet")

    # 4. COMBO_A3_G05_REPORT.pdf
    report_md = (root / "docs" / "REPORT_DRAFT.md").read_text()
    create_pdf_from_markdown_sections(report_md, root / "docs" / "COMBO_A3_G05_REPORT.pdf", "AgriSoko Pocket Report")


if __name__ == "__main__":
    main()

