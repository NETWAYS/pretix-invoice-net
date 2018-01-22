# Pretix Invoice Renderer for NETWAYS
#
# Copyright 2018 NETWAYS GmbH <support@netways.de>
# Copyright 2017 Raphael Michel <mail@raphaelmichel.de>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections import defaultdict
from decimal import Decimal
from io import BytesIO
from typing import Tuple

import vat_moss.exchange_rates
from django.contrib.staticfiles import finders
from django.dispatch import receiver
from django.utils.formats import date_format, localize
from django.utils.translation import pgettext

from reportlab.lib import pagesizes
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle, StyleSheet1
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (
    BaseDocTemplate, Frame, KeepTogether, NextPageTemplate, PageTemplate,
    Paragraph, Spacer, Table, TableStyle,
)

#http://matthiaseisen.com/pp/patterns/p0156/
from reportlab.lib import colors

from pretix.base.decimal import round_decimal
from pretix.base.models import Event, Invoice
from pretix.base.signals import register_invoice_renderers

from pretix.base.invoice import BaseReportlabInvoiceRenderer

class NetInvoiceRenderer(BaseReportlabInvoiceRenderer):
    identifier = 'netways'
    verbose_name = pgettext('invoice', 'NETWAYS invoice renderer')

    def _on_other_page(self, canvas: Canvas, doc):
        canvas.saveState()
        canvas.setFont('OpenSans', 8)
        canvas.drawRightString(self.pagesize[0] - 20 * mm, 10 * mm, pgettext("invoice", "Page %d") % (doc.page,))

        for i, line in enumerate(self.invoice.footer_text.split('\n')[::-1]):
            canvas.drawCentredString(self.pagesize[0] / 2, 25 + (3.5 * i) * mm, line.strip())

        canvas.restoreState()

    def _on_first_page(self, canvas: Canvas, doc):
        canvas.setCreator('NETWAYS')
        canvas.setTitle(pgettext('invoice', 'Invoice {num}').format(num=self.invoice.number))

        canvas.saveState()
        canvas.setFont('OpenSans', 8)
        canvas.drawRightString(self.pagesize[0] - 20 * mm, 10 * mm, pgettext("invoice", "Page %d") % (doc.page,))

        for i, line in enumerate(self.invoice.footer_text.split('\n')[::-1]):
            canvas.drawCentredString(self.pagesize[0] / 2, 25 + (3.5 * i) * mm, line.strip())

        # Left, Invoice From
        textobject = canvas.beginText(25 * mm, (297 - 15) * mm)
        textobject.setFont('OpenSansBd', 8)
        textobject.textLine(pgettext('invoice', 'Invoice from').upper())
        canvas.drawText(textobject)

        p = Paragraph(self.invoice.invoice_from.strip().replace('\n', '<br />\n'), style=self.stylesheet['Normal'])
        p.wrapOn(canvas, 70 * mm, 50 * mm)
        p_size = p.wrap(70 * mm, 50 * mm)
        p.drawOn(canvas, 25 * mm, (297 - 17) * mm - p_size[1])

        # Left, Invoice To
        textobject = canvas.beginText(25 * mm, (297 - 50) * mm)
        textobject.setFont('OpenSansBd', 8)
        textobject.textLine(pgettext('invoice', 'Invoice to').upper())
        canvas.drawText(textobject)

        p = Paragraph(self.invoice.invoice_to.strip().replace('\n', '<br />\n'), style=self.stylesheet['Normal'])
        p.wrapOn(canvas, 85 * mm, 50 * mm)
        p_size = p.wrap(85 * mm, 50 * mm)
        p.drawOn(canvas, 25 * mm, (297 - 52) * mm - p_size[1])


        rightX = 95 * mm;

        # Right, Order code
        textobject = canvas.beginText(rightX, (297 - 38) * mm)
        textobject.setFont('OpenSansBd', 8)
        textobject.textLine(pgettext('invoice', 'Order code').upper())
        textobject.moveCursor(0, 5)
        textobject.setFont('OpenSans', 10)
        textobject.textLine(self.invoice.order.full_code)
        canvas.drawText(textobject)

        # Right, * number
        textobject = canvas.beginText(rightX, (297 - 50) * mm)
        textobject.setFont('OpenSansBd', 8)
        if self.invoice.is_cancellation:
            textobject.textLine(pgettext('invoice', 'Cancellation number').upper())
            textobject.moveCursor(0, 5)
            textobject.setFont('OpenSans', 10)
            textobject.textLine(self.invoice.number)
            textobject.moveCursor(0, 5)
            textobject.setFont('OpenSansBd', 8)
            textobject.textLine(pgettext('invoice', 'Original invoice').upper())
            textobject.moveCursor(0, 5)
            textobject.setFont('OpenSans', 10)
            textobject.textLine(self.invoice.refers.number)
        else:
            textobject.textLine(pgettext('invoice', 'Invoice number').upper())
            textobject.moveCursor(0, 5)
            textobject.setFont('OpenSans', 10)
            textobject.textLine(self.invoice.number)
        textobject.moveCursor(0, 5)

        # Right, * date
        if self.invoice.is_cancellation:
            textobject.setFont('OpenSansBd', 8)
            textobject.textLine(pgettext('invoice', 'Cancellation date').upper())
            textobject.moveCursor(0, 5)
            textobject.setFont('OpenSans', 10)
            textobject.textLine(date_format(self.invoice.date, "DATE_FORMAT"))
            textobject.moveCursor(0, 5)
            textobject.setFont('OpenSansBd', 8)
            textobject.textLine(pgettext('invoice', 'Original invoice date').upper())
            textobject.moveCursor(0, 5)
            textobject.setFont('OpenSans', 10)
            textobject.textLine(date_format(self.invoice.refers.date, "DATE_FORMAT"))
            textobject.moveCursor(0, 5)
        else:
            textobject.setFont('OpenSansBd', 8)
            textobject.textLine(pgettext('invoice', 'Invoice date').upper())
            textobject.moveCursor(0, 5)
            textobject.setFont('OpenSans', 10)
            textobject.textLine(date_format(self.invoice.date, "DATE_FORMAT"))
            textobject.moveCursor(0, 5)

        canvas.drawText(textobject)

        # Right, Invoice and Event Logo
        rightLogoX = 160 * mm

        if self.invoice.event.settings.logo_image:
            logo_file = self.invoice.event.settings.get('logo_image', binary_file=True)
            canvas.drawImage(ImageReader(logo_file),
                             rightLogoX, (297 - 38) * mm,
                             width=25 * mm, height=25 * mm,
                             preserveAspectRatio=True, anchor='n',
                             mask='auto')

        if self.invoice.event.settings.invoice_logo_image:
            logo_file = self.invoice.event.settings.get('invoice_logo_image', binary_file=True)
            canvas.drawImage(ImageReader(logo_file),
                             rightLogoX, (297 - 63) * mm,
                             width=25 * mm, height=25 * mm,
                             preserveAspectRatio=True, anchor='n',
                             mask='auto')

        # Right, Event
        if self.invoice.event.settings.show_date_to:
            p_str = (
                str(self.invoice.event.name) + '\n' + pgettext('invoice', '{from_date}\nuntil {to_date}').format(
                    from_date=self.invoice.event.get_date_from_display(),
                    to_date=self.invoice.event.get_date_to_display())
            )
        else:
            p_str = (
                str(self.invoice.event.name) + '\n' + self.invoice.event.get_date_from_display()
            )

        p = Paragraph(p_str.strip().replace('\n', '<br />\n'), style=self.stylesheet['Normal'])
        p.wrapOn(canvas, 65 * mm, 50 * mm)
        p_size = p.wrap(65 * mm, 50 * mm)
        p.drawOn(canvas, 95 * mm, (297 - 17) * mm - p_size[1])

        textobject = canvas.beginText(rightX, (297 - 15) * mm)
        textobject.setFont('OpenSansBd', 8)
        textobject.textLine(pgettext('invoice', 'Event').upper())
        canvas.drawText(textobject)

        canvas.restoreState()

    def _get_first_page_frames(self, doc):
        footer_length = 3.5 * len(self.invoice.footer_text.split('\n')) * mm
        return [
            Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 75 * mm,
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=footer_length,
                  id='normal')
        ]

    def _get_other_page_frames(self, doc):
        footer_length = 3.5 * len(self.invoice.footer_text.split('\n')) * mm
        return [
            Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=footer_length,
                  id='normal')
        ]

    def _get_story(self, doc):
        story = [
            NextPageTemplate('FirstPage'),
            Paragraph(pgettext('invoice', 'Invoice')
                      if not self.invoice.is_cancellation
                      else pgettext('invoice', 'Cancellation'),
                      self.stylesheet['Heading1']),
            Spacer(1, 5 * mm),
            NextPageTemplate('OtherPages'),
        ]

        if self.invoice.internal_reference:
            story.append(Paragraph(
                pgettext('invoice', 'Your reference: {reference}').format(reference=self.invoice.internal_reference),
                self.stylesheet['Normal']
            ))

        if self.invoice.introductory_text:
            story.append(Paragraph(self.invoice.introductory_text, self.stylesheet['Normal']))
            story.append(Spacer(1, 10 * mm))

        # Table
        taxvalue_map = defaultdict(Decimal)
        grossvalue_map = defaultdict(Decimal)

        tstyledata = [
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, 0), 'OpenSansBd'),
            ('FONTNAME', (0, -1), (-1, -1), 'OpenSansBd'),
            ('LEFTPADDING', (0, 0), (0, -1), 0),
            ('RIGHTPADDING', (-1, 0), (-1, -1), 0),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.gray), #NET specific styling
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ]
        tdata = [(
            pgettext('invoice', 'Description'),
            pgettext('invoice', 'Qty.'), #NET specific
            pgettext('invoice', 'Tax rate'),
            pgettext('invoice', 'Net'),
            pgettext('invoice', 'Gross'),
        )]
        total = Decimal('0.00')
        for line in self.invoice.lines.all():
            tdata.append((
                Paragraph(line.description, self.stylesheet['Normal']),
                localize(1), #NET specific
                localize(line.tax_rate) + " %",
                localize(line.net_value) + " " + self.invoice.event.currency,
                localize(line.gross_value) + " " + self.invoice.event.currency,
            ))
            taxvalue_map[line.tax_rate, line.tax_name] += line.tax_value
            grossvalue_map[line.tax_rate, line.tax_name] += line.gross_value
            total += line.gross_value

        tdata.append([
            pgettext('invoice', 'Invoice total'), '', '', localize(total) + " " + self.invoice.event.currency
        ])
        colwidths = [a * doc.width for a in (.45, .10, .15, .15, .15)] #NET specific
        table = Table(tdata, colWidths=colwidths, repeatRows=1)
        table.setStyle(TableStyle(tstyledata))
        story.append(table)

        story.append(Spacer(1, 15 * mm))

        if self.invoice.payment_provider_text:
            story.append(Paragraph(self.invoice.payment_provider_text, self.stylesheet['Normal']))

        if self.invoice.additional_text:
            story.append(Paragraph(self.invoice.additional_text, self.stylesheet['Normal']))
            story.append(Spacer(1, 15 * mm))

        tstyledata = [
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('LEFTPADDING', (0, 0), (0, -1), 0),
            ('RIGHTPADDING', (-1, 0), (-1, -1), 0),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('FONTNAME', (0, 0), (-1, -1), 'OpenSans'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.gray), #NET specific styling
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ]
        thead = [
            pgettext('invoice', 'Tax rate'),
            pgettext('invoice', 'Net value'),
            pgettext('invoice', 'Gross value'),
            pgettext('invoice', 'Tax'),
            ''
        ]
        tdata = [thead]

        for idx, gross in grossvalue_map.items():
            rate, name = idx
            if rate == 0:
                continue
            tax = taxvalue_map[idx]
            tdata.append([
                localize(rate) + " % " + name,
                localize(gross - tax) + " " + self.invoice.event.currency,
                localize(gross) + " " + self.invoice.event.currency,
                localize(tax) + " " + self.invoice.event.currency,
                ''
            ])

        def fmt(val):
            try:
                return vat_moss.exchange_rates.format(val, self.invoice.foreign_currency_display)
            except ValueError:
                return localize(val) + ' ' + self.invoice.foreign_currency_display

        if len(tdata) > 1:
            colwidths = [a * doc.width for a in (.25, .15, .15, .15, .3)]
            table = Table(tdata, colWidths=colwidths, repeatRows=2, hAlign=TA_LEFT)
            table.setStyle(TableStyle(tstyledata))
            story.append(KeepTogether([
                Paragraph(pgettext('invoice', 'Included taxes'), self.stylesheet['FineprintHeading']),
                table
            ]))

            if self.invoice.foreign_currency_display and self.invoice.foreign_currency_rate:
                tdata = [thead]

                for idx, gross in grossvalue_map.items():
                    rate, name = idx
                    if rate == 0:
                        continue
                    tax = taxvalue_map[idx]
                    gross = round_decimal(gross * self.invoice.foreign_currency_rate)
                    tax = round_decimal(tax * self.invoice.foreign_currency_rate)
                    net = gross - tax

                    tdata.append([
                        localize(rate) + " % " + name,
                        fmt(net), fmt(gross), fmt(tax), ''
                    ])

                table = Table(tdata, colWidths=colwidths, repeatRows=2, hAlign=TA_LEFT)
                table.setStyle(TableStyle(tstyledata))

                story.append(KeepTogether([
                    Spacer(1, height=2 * mm),
                    Paragraph(
                        pgettext(
                            'invoice', 'Using the conversion rate of 1:{rate} as published by the European Central Bank on '
                                       '{date}, this corresponds to:'
                        ).format(rate=localize(self.invoice.foreign_currency_rate),
                                 date=date_format(self.invoice.foreign_currency_rate_date, "SHORT_DATE_FORMAT")),
                        self.stylesheet['Fineprint']
                    ),
                    Spacer(1, height=3 * mm),
                    table
                ]))
        elif self.invoice.foreign_currency_display and self.invoice.foreign_currency_rate:
            story.append(Spacer(1, 5 * mm))
            story.append(Paragraph(
                pgettext(
                    'invoice', 'Using the conversion rate of 1:{rate} as published by the European Central Bank on '
                               '{date}, the invoice total corresponds to {total}.'
                ).format(rate=localize(self.invoice.foreign_currency_rate),
                         date=date_format(self.invoice.foreign_currency_rate_date, "SHORT_DATE_FORMAT"),
                         total=fmt(total)),
                self.stylesheet['Fineprint']
            ))

        return story


