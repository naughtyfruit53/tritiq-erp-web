# src/services/document_utils.py
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.graphics.shapes import Drawing, Line
from reportlab.graphics import renderPDF
from reportlab.pdfgen.canvas import Canvas
from reportlab.graphics.barcode import qr
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.rl_config import defaultPageSize
from PIL import Image
import os
import logging

logger = logging.getLogger(__name__)

PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH = defaultPageSize[0]

class CustomDocTemplate(SimpleDocTemplate):
    def __init__(self, filename, **kw):
        super().__init__(filename, **kw)
        self.elements = []

def get_paragraph_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='small', fontSize=8, leading=10))
    styles.add(ParagraphStyle(name='medium', fontSize=10, leading=12))
    styles.add(ParagraphStyle(name='large', fontSize=12, leading=14))
    return styles

def create_logo(company_data):
    logo_path = company_data[9] if len(company_data) > 9 and company_data[9] else None
    if logo_path and os.path.exists(logo_path):
        image = Image.open(logo_path)
        image_width = image.width
        image_height = image.height
        aspect_ratio = image_width / image_height
        max_height = 20 * mm
        height = max_height
        width = height * aspect_ratio
        return Image(logo_path, width=width, height=height)
    return Paragraph("Logo", get_paragraph_styles()['small'])

def create_header_table(company_data, title, header_fields, styles):
    logo = create_logo(company_data)
    company_info = Paragraph(f"""
    <b>{company_data[0]}</b><br/>
    {company_data[1]}<br/>
    {company_data[2] or ''}<br/>
    {company_data[3]}, {company_data[4]} - {company_data[5]}<br/>
    GSTIN: {company_data[6] or 'N/A'}<br/>
    Contact: {company_data[7]} | Email: {company_data[8] or 'N/A'}
    """, styles['small'])
    header_info = Paragraph(f"<b>{title}</b>", styles['medium'])
    for field in header_fields:
        header_info += Paragraph(f"{field['label']}: {field['value']}", styles['small'])
    header_data = [
        [logo, company_info, header_info]
    ]
    header_table = Table(header_data, colWidths=[40 * mm, 85 * mm, 60 * mm])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    return header_table

def create_party_table(party_data, party_type, company_data, styles):
    party_info = Paragraph(f"""
    <b>{party_type}:</b><br/>
    {party_data[0]}<br/>
    {party_data[1]}<br/>
    {party_data[2] or ''}<br/>
    {party_data[3]}, {party_data[4]} - {party_data[5]}<br/>
    GSTIN: {party_data[6] or 'N/A'}<br/>
    Contact: {party_data[7] or 'N/A'}
    """, styles['small'])
    company_address = Paragraph(f"""
    <b>Our Address:</b><br/>
    {company_data[1]}<br/>
    {company_data[2] or ''}<br/>
    {company_data[3]}, {company_data[4]} - {company_data[5]}<br/>
    GSTIN: {company_data[6] or 'N/A'}
    """, styles['small'])
    party_data = [
        [party_info, company_address]
    ]
    party_table = Table(party_data, colWidths=[85 * mm, 85 * mm])
    party_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    return party_table

def create_items_table(headers, items, styles):
    data = [headers]
    col_widths = [20 * mm] + [30 * mm] * (len(headers) - 1)
    for idx, item in enumerate(items, 1):
        row = [idx] + list(item)
        data.append(row)
    items_table = Table(data, colWidths=col_widths)
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    return items_table, col_widths

def create_totals_and_terms_table(totals, terms, styles, col_widths):
    totals_data = totals
    totals_table = Table(totals_data, colWidths=[col_widths[-2], col_widths[-1]])
    totals_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('LINEABOVE', (0, 0), (-1, 0), 0.5, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), 0.5, colors.black),
    ]))
    terms_paragraph = Paragraph("Terms & Conditions: " + " ".join(terms), styles['small'])
    full_table_data = [[totals_table, terms_paragraph]]
    full_table = Table(full_table_data, colWidths=[sum(col_widths[-2:]), sum(col_widths[:-2])])
    full_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    return full_table

def create_amount_in_words_table(amount, label, styles, number_to_words):
    amount_words = number_to_words(amount)
    amount_words_paragraph = Paragraph(f"{label}: {amount_words}", styles['small'])
    amount_words_table = Table([[amount_words_paragraph]], colWidths=[165.77 * mm])
    amount_words_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    return amount_words_table

def create_signatory_table(company_name, styles):
    signatory_data = [
        [Paragraph("For " + company_name, styles['small'])]
    ]
    signatory_table = Table(signatory_data, colWidths=[165.77 * mm])
    signatory_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ]))
    return signatory_table