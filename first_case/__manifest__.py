{
    "name": "First Case",
    "author": "Antonio Martin",
    "category": "Uncategorized",
    'license' : "LGPL-3",
    "version": "16.0.0.0.1",
    "depends": ['project', 'second_case'],
    "test": [],
    "data": [
        "data/project_data.xml",
        "views/project_views.xml",
        "views/res_config_settings_views.xml"
    ],
    "demo": [],
    "assets": {
        "web.assets_backend": [
            "first_case/static/src/js/project_calendar_controller.js",
        ],
    },
    "installable": True,
    "auto_install": False,
    "application": True,
}
