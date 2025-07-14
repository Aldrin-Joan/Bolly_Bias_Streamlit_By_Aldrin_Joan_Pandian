# modules/report_generation.py

import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
import os

def generate_feedback_report(input_csv_path):
    df = pd.read_csv(input_csv_path)
    df = df[df['stereotype_type'] != 'none'].copy()

    severity_map = {
        "appearance_focus": 2,
        "relationship_only": 2,
        "agency_gap": 3,
        "occupation_gap": 3,
    }
    df["severity_score"] = df["stereotype_type"].map(severity_map).fillna(1)
    df["rewrite"] = df["rewritten_line"]
    df["rank"] = df["severity_score"].rank(method="dense", ascending=False).astype(int)

    # Output paths
    csv_output_path = os.path.join("data", "feedback_report.csv")
    pdf_output_path = os.path.join("data", "feedback_report.pdf")

    # Save CSV
    df.to_csv(csv_output_path, index=False)

    # Build PDF
    doc = SimpleDocTemplate(pdf_output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("🎬 Bollywood Bias Buster – Script Feedback Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    data = [["#", "Original Line", "Stereotype", "Severity", "Rewritten Line"]]

    for idx, row in df.sort_values("rank").iterrows():
        data.append([
            row["rank"],
            row["line"],
            row["stereotype_type"],
            int(row["severity_score"]),
            row["rewrite"]
        ])

    table = Table(data, colWidths=[30, 160, 85, 60, 180])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
    ]))

    for i in range(1, len(data)):
        if int(data[i][3]) >= 3:
            table.setStyle([("BACKGROUND", (0, i), (-1, i), colors.lightpink)])

    elements.append(table)
    doc.build(elements)

    return csv_output_path, pdf_output_path
