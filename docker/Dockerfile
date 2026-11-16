FROM odoo:18.0

USER root
COPY addons/tucha_crm /opt/tucha-addons/tucha_crm
COPY docker/odoo.conf /etc/odoo/odoo.conf
COPY docker/start-sandbox.sh /usr/local/bin/start-sandbox
RUN chmod 0755 /usr/local/bin/start-sandbox \
    && chown -R odoo:odoo /opt/tucha-addons/tucha_crm
USER odoo

ENTRYPOINT ["/usr/local/bin/start-sandbox"]
