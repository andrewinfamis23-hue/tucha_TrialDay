{
    "name": "TuchaCRM Sandbox",
    "version": "18.0.1.0.0",
    "summary": "Изолированный учебный срез CRM",
    "category": "Training",
    "license": "LGPL-3",
    "depends": ["base", "web"],
    "data": [
        "security/groups.xml",
        "security/ir.model.access.csv",
        "views/views.xml",
    ],
    "post_init_hook": "post_init_hook",
    "application": True,
    "installable": True,
}
