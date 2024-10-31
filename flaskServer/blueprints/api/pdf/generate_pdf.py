import datetime
from flask import Blueprint, session, request, jsonify, send_file

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import blueprints.db

pdfStyles = getSampleStyleSheet()

bp = Blueprint("generate_pdf", __name__, static_folder="static", template_folder="templates")

@bp.route("/api/generate_pdf", methods=["POST"]) 
def on_get_qualifications():
    

    if not session["user_ID"]:
        #HTTPS Code: Forbidden
        return jsonify({"error_message" : "No user is logged in"}), 403
    
    data = request.json
    qualification_id = data.get("qualification_id")
    user_id = session["user_ID"]
    
    
    if not blueprints.db.check_if_user_has_done_all_sessions(user_id, qualification_id):
        #HTTPS Code: Forbidden
        return jsonify({"error_message" : "User did not done all sessions"}), 403

    
    
    
    qualification_titel = blueprints.db.get_qualifications_titel(qualification_id)
    qualification_titel = qualification_titel[0][0]
    
    user_name = blueprints.db.get_user_name(user_id)

    
    
    pdf_table_data = blueprints.db.get_qualification_pdf_table(qualification_id, user_id)
    
    
    
    
    
    
    
    
    
    
    pdf_file = generate_PDF(user_name[0], user_name[1], qualification_titel, pdf_table_data)
    filename = "Nachweis.pdf"
    return send_file(pdf_file, as_attachment=False, download_name=filename)


def generate_PDF(first_name, last_name, qualification_titel, pdf_table_data):
    
    buffer = BytesIO()
    
    
    for i in range(len(pdf_table_data)):
        timestamp = datetime.datetime.fromisoformat(pdf_table_data[i][2])
        pdf_table_data[i] = (pdf_table_data[i][0],pdf_table_data[i][1], f"{timestamp.day}.{timestamp.month}.{timestamp.year}")
    
    doc = SimpleDocTemplate(buffer)
    
    
    style_normal = pdfStyles["Normal"]
    style_title = pdfStyles["Title"]
    
    elements = []
    

    # Titel
    elements.append(Paragraph("Persönlicher Nachweis über die Teilnahme an der modularen Grundlagenausbildung", style_title))
    elements.append(Spacer(1, 20))
    
    
    # Name des Teilnehmers
    elements.append(Paragraph(f"{first_name} {last_name}", style_normal))
    elements.append(Spacer(1, 20))
    
    # Qualifikation
    elements.append(Paragraph("Die Kompetenzen der Qualifikationsstufe", style_normal))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"„{qualification_titel}“", style_normal))
    elements.append(Spacer(1, 10))
    
    
    
    # Datum und FwDV2 Hinweis
    elements.append(Paragraph("Gemäß FwDV2, RdErl. d. MI v. 17.11.2023 – 34.2-13221/2.1", style_normal))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"wurden am {datetime.datetime.today().strftime('%d.%m.%Y')} erfolgreich nachgewiesen.", style_normal))
    elements.append(Spacer(1, 40))
    
    
    elements.append(Paragraph("Abgeschlossene Unterrichtsstunden:", style_normal))
    elements.append(Spacer(1, 20))
    
    pdf_table_data.insert(0, ("Modul", "Ausbildungseinheit", "Abschlussdatum"))
    
    
    table = Table(pdf_table_data)
    # (-1, -1) bedeutet: alle Zeilen und Spalten bis zum Ende der Tabelle
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alle Zellen zentrieren
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fettgedruckte Kopfzeile
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Abstand in der Kopfzeile
        ('GRID', (0, 0), (-1, -1), 1, colors.black)  # Schwarzer Rahmen um die ganze Tabelle
    ]))

    elements.append(table)
    
    doc.build(elements)
    
    buffer.seek(0)
    
    

    return buffer