from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def generate_quotation_pdf(
    customer_name,
    customer_phone,
    items,
):
    """
    Generate a customer quotation PDF in memory.
    """

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
    )

    styles = getSampleStyleSheet()
    story = []

    # --------------------------------------------------
    # COMPANY DETAILS
    # --------------------------------------------------

    story.append(
        Paragraph(
            "<b>DIAMOND PANS LIMITED</b>",
            styles["Title"],
        )
    )

    story.append(
        Paragraph(
            "C TO C Filling Station, Emene<br/>"
            "Opposite Airport, Enugu State, Nigeria",
            styles["Normal"],
        )
    )

    story.append(Spacer(1, 10 * mm))

    # --------------------------------------------------
    # QUOTATION INFORMATION
    # --------------------------------------------------

    now = datetime.now()

    quotation_number = now.strftime(
        "QT-%Y%m%d-%H%M%S"
    )

    quotation_date = now.strftime(
        "%d/%m/%Y"
    )

    story.append(
        Paragraph(
            "<b>QUOTATION</b>",
            styles["Heading1"],
        )
    )

    story.append(
        Paragraph(
            f"<b>Quotation No:</b> {quotation_number}<br/>"
            f"<b>Date:</b> {quotation_date}",
            styles["Normal"],
        )
    )

    story.append(Spacer(1, 5 * mm))

    # --------------------------------------------------
    # CUSTOMER DETAILS
    # --------------------------------------------------

    display_name = (
        customer_name.strip()
        if customer_name.strip()
        else "Customer"
    )

    display_phone = (
        customer_phone.strip()
        if customer_phone.strip()
        else "-"
    )

    story.append(
        Paragraph(
            f"<b>Customer:</b> {display_name}<br/>"
            f"<b>Phone:</b> {display_phone}",
            styles["Normal"],
        )
    )

    story.append(Spacer(1, 8 * mm))

    # --------------------------------------------------
    # ITEMS TABLE
    # --------------------------------------------------

    table_data = [
        [
            "Description",
            "Qty",
            "Unit Price",
            "Total",
        ]
    ]

    grand_total = 0

    for item in items:

        description = (
            f'{item["original_length"]:g}" x '
            f'{item["original_width"]:g}" '
            f'({item["thickness"]})'
        )

        quantity = item["quantity"]
        unit_price = item["unit_price"]
        total_price = item["total_price"]

        grand_total += total_price

        table_data.append(
            [
                description,
                str(quantity),
                f"N{unit_price:,.0f}",
                f"N{total_price:,.0f}",
            ]
        )

    table_data.append(
        [
            "",
            "",
            "GRAND TOTAL",
            f"N{grand_total:,.0f}",
        ]
    )

    table = Table(
        table_data,
        colWidths=[
            75 * mm,
            18 * mm,
            35 * mm,
            35 * mm,
        ],
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey,
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.black,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "FONTNAME",
                    (2, -1),
                    (-1, -1),
                    "Helvetica-Bold",
                ),
                (
                    "ALIGN",
                    (1, 0),
                    (-1, -1),
                    "RIGHT",
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    story.append(table)

    story.append(Spacer(1, 12 * mm))

    # --------------------------------------------------
    # FOOTER
    # --------------------------------------------------

    story.append(
        Paragraph(
            "Thank you for your business.",
            styles["Normal"],
        )
    )

    document.build(story)

    buffer.seek(0)

    return buffer.getvalue(), quotation_number