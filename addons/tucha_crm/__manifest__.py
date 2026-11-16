{
    "name": "TuchaCRM Sandbox",
    "version": "18.0.1.0.0",
    "summary": "Изолированный учебный срез CRM",
    "category": "Training",
    "license": "LGPL-3",
    "depends": ["base", "web"],
    "data": [
        "data/sandbox_language.xml",
        "security/groups.xml",
        "security/ir.model.access.csv",
        "views/views.xml",
        "views/interface.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "tucha_crm/static/src/css/tucha_theme.css",
            "tucha_crm/static/src/css/fix_layout.css",
            "tucha_crm/static/src/js/section_navigation.js",
            "tucha_crm/static/src/js/sandbox_interface.js",
            "tucha_crm/static/src/xml/sandbox_interface.xml",
        ],
        "web.assets_frontend": [
            "tucha_crm/static/src/css/tucha_theme.css",
        ],
    },
    "post_init_hook": "post_init_hook",
    "application": True,
    "installable": True,
}
