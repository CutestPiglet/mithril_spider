# -*- coding: utf-8 -*-
import scrapy

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP

import smtp_settings


class MithrilSpider(scrapy.Spider):
    name = 'mithril_spider'
    start_urls = ['https://max.maicoin.com/markets/mithtwd']

    def parse(self, response):
        # SMTP settings
        smtp = SMTP(smtp_settings.SMTP_HOST, smtp_settings.SMTP_HOST_PORT)
        smtp.starttls()
        smtp.login(smtp_settings.EMAIL_USERNAME, smtp_settings.EMAIL_PASSWORD)
        sender = smtp_settings.EMAIL_USERNAME
        recipients = ['johnmay0629@gmail.com', 'faerieeven.wang@gmail.com']

        # message container
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)

        try:
            # get mithril price
            mith_price = float(response.xpath('//*[@id="market-list-mithtwd"]/td[2]//text()').extract_first())
        except Exception as e:
            msg['Subject'] = 'Error！'
            text = MIMEText('Get Mithril price error: {}'.format(str(e)))
            msg.attach(text)
            smtp.sendmail(sender, recipients, msg.as_string())
            smtp.quit()

        mith_threshold_price = 20
        if mith_price >= mith_threshold_price:
            msg['Subject'] = '秘銀現在一顆 {} 元，超過門檻值 {} 元拉！'.format(mith_price, mith_threshold_price)
            text = MIMEText('快去賣！')
            msg.attach(text)
            smtp.sendmail(sender, recipients, msg.as_string())
            smtp.quit()
