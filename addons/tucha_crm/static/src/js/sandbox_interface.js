/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useBus } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";
import { NavBar } from "@web/webclient/navbar/navbar";
import { UserMenu } from "@web/webclient/user_menu/user_menu";
import { user } from "@web/core/user";
import { isTuchaSectionActionActive } from "./section_navigation";
import "@web/webclient/user_menu/user_menu_items";

// Адаптер PROD-интерфейса к учебным моделям. Сетевых адресов PROD здесь нет.
const userMenu = registry.category("user_menuitems");
const settingsItem = userMenu.get("profile");
const logoutItem = userMenu.get("log_out");
for (const [key] of userMenu.getEntries()) userMenu.remove(key);

userMenu.add("tucha_account", (env) => ({
    id: "tucha_account", type: "item", description: "Учётная запись", sequence: 10,
    callback: () => env.services.action.doAction({
        type: "ir.actions.act_window", name: "Учётная запись",
        res_model: "res.partner", res_id: user.partnerId,
        views: [[false, "form"]], view_mode: "form", target: "current",
    }),
}));
userMenu.add("tucha_information", (env) => ({
    id: "tucha_information", type: "item", description: "Информация", sequence: 20,
    callback: () => env.services.notification.add(
        "Изолированная учебная CRM. Здесь используются только фейковые данные.",
        { title: "TuchaCRM Sandbox", type: "info" },
    ),
}));
userMenu.add("tucha_settings", (env) => ({
    ...settingsItem(env), id: "tucha_settings", description: "Настройки", sequence: 30,
}));
userMenu.add("tucha_logout", (env) => ({
    ...logoutItem(env), id: "tucha_logout", description: "Выход", sequence: 40,
}));

const allowedUserMenuIds = new Set([
    "tucha_account", "tucha_information", "tucha_settings", "tucha_logout",
]);
patch(UserMenu.prototype, {
    getElements() {
        return super.getElements().filter((item) => allowedUserMenuIds.has(item.id));
    },
});

registry.category("services").add("tucha_sandbox_branding", {
    dependencies: ["title"],
    start(env, { title }) {
        title.setParts({ tucha: "Туча-МЛ · Sandbox" });
    },
});

patch(NavBar.prototype, {
    setup() {
        super.setup();
        useBus(this.env.bus, "ACTION_MANAGER:UI-UPDATED", () => this.render());
    },
    isTuchaSectionActive(section) {
        return isTuchaSectionActionActive(
            section, this.actionService.currentController?.action,
        );
    },
});
