from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


file_name = "pdfTest.pdf"

c = canvas.Canvas(file_name, pagesize=letter)

c.setTitle("Nachweis")
c.drawCentredString(300, 770, "Persönlicher Nachweis über die Teilnahme an der modularen Grundlagenausbildung")


c.drawCentredString(300, 740, "Vorname Nachname xx.xx.xxxx Feuerwehr xxxxxxxxxxxxxx")

c.drawCentredString(300, 700, "Die Kompetenzen der Qualifikationsstufe 1")

c.drawCentredString(300, 675, " „Einsatzfähigkeit“ ") # Qulaification type

c.drawCentredString(300, 650, "Gemäß FwDV2, RdErl. d. MI v. 17.11.2023 – 34.2-13221/2.1 ")

c.drawCentredString(300, 630, "wurden am 15.06.2024 erfolgreich nachgewiesen.") 


c.save()
