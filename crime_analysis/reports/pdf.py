# reports/pdf.py

from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse

def export_metrics_pdf(metrics_table, filename="metrics_report.pdf"):
    """
    Generates a PDF from a Pandas DataFrame of metrics and returns it as HttpResponse.
    """
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 50, "Metrics Report")

    # Draw table
    y = height - 80
    p.setFont("Helvetica", 12)
    for idx, row in metrics_table.iterrows():
        text = ", ".join([str(item) for item in row])
        p.drawString(50, y, text)
        y -= 20

        if y < 50:
            p.showPage()
            y = height - 50

    p.save()
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    response.write(pdf)
    return response

