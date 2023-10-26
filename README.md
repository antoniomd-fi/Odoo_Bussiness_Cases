# Odoo_Bussiness_Cases

## DEMO

https://github.com/antoniomd-fi/Odoo_Bussiness_Cases/assets/90221784/5246bd74-0b53-4309-b963-a01410f6427e

## Case 1
One of our customers uses the project module, they have construction sites and
divisions for each of their construction projects. Each Site has a certain number of
divisions (Odoo’s task)that need to be delivered in order.

**Requirements**

Create an inheritance module.
1. Change all the labels ‘Project/s’ in the project module to ‘Site/s’ (Menu, field
label)
2. Change all the labels ‘Task/s’ in the project module to ‘Milestone/s’ (Menu,
field label)
3. Currently in Project menu only displays the Kanban view
a. Add list view which will display as the main view when opening the Site
(Project) menu
b. When clicking data in the list view it will open the form view (form view
(XML) already exists in base Odoo)
c. When selecting the button Create it should display create mode in form
view, not Kanban view

4. Add some new fields in the Site (project)
   - Deadline : Date DateTime
   - Budget : Float
   - Project : Size Selection (small, medium, large)
   - Stage ID : Many2one to "site.stage", stage should be displayed in all Site
     
5. Set Kanban view of Site(Project) like Kanban of divisions (Task) which both groups by stage by default


## Case 2
When the site moves to a specific stage, the user wants some field to be filled
(mandatory). The mandatory field for every stage can be different

**Requirement**

Create new module
1. Create new object dynamic.requirement.field and
dynamic.requirement.field.line
2. Create some fields for dynamic.requirement.field:
   - Sequence : Int, default=10
   - Type : Selection (Site, Milestone), mandatory
   - Name : Char, default="New", Copy = False, mandatory
   - Active : Boolean, default="True"
   - Mandatory Project Line : One2many to "dynamic.requirement.field.line"
   - Company : Many2one to "company" default to company's active
3. Create some fields for dynamic.requirement.field.line:
   - Sequence : Int, default 10
   - Requirement Mandatory Project :Many2one to "dynamic.requirement.field"
   - Stage : Many2one to "site.stages"
   - Mandatory : Fields Many2many to "ir.model.fields"
   - Custom Warning Message : Char, mandatory
   - Company : Many2one to company, default to company's active
4. Add the new menu ‘Requirements’ under menu Configuration in Site(Project)
5. This menu will have a list view and form view (default list view)
  - For the List View, display the following fields:
    - Name
    - Type
    - Company
    - Active
    - Form form view please set it like this:
      ![form](https://github.com/antoniomd-fi/Odoo_Bussiness_Cases/assets/90221784/6d39aa77-bd89-4bc4-a4e2-bf38565d0d1b)
6. Add a new field in Site(project)
  - Requirement (Many2one, object=dynamic.requirement.field)
7. Create function than when moving Site(project) through with logic like this
  - If a requirement field is set on the Site(project), when we move Site to another stage it should check the conditions.
  - If the destination stage (next stage) is set on the conditions, we should check if all fields set in Mandatory fields are filled.
  - If all fields are not filled we should display pop up warning with information fields not fill based on field Custom Warning Msg
    - Example = “Fields Customer, Dateline is mandatory”
