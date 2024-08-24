
# Material Module


## Description:
This odoo14 Module has 2 model
- om.materials
- om.suppliers 

Materials has relation to suppliers by supplier_id.

This module is used for store data materials and suppliers.

this module create for odoo 14 with python 3.9

## Instructions:
add this module to addons folder and register the addons path to config(example config is provided).
Place config to odoo main path (next to odoo-bin)

This module provide controller(web) and model view:
- model view can be access in material menu in apps
- website view can be access from '/material/view' and '/supplier/view'

run command
```
    # for unit test
    python odoo-bin -c ../odoo.conf  --test-enable --stop-after-init --test-tags=material_note
    
    # for running application
    python odoo-bin -c ../odoo.conf -u material_note  
    
    # for running application and import demo data
    python odoo-bin -c ../odoo.conf -u material_note  -i material_note

```
