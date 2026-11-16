/** @odoo-module **/

export function isTuchaSectionActionActive(section, action) {
    if (!section.xmlid?.startsWith("tucha_crm.") || !action) return false;
    const includesAction = (menu) =>
        menu.actionID === action.id || menu.childrenTree?.some(includesAction);
    return Boolean(action.id && includesAction(section));
}
