import Alpine from "alpinejs";
import mask from "@alpinejs/mask";
import tippy from "tippy.js";
import "boxicons";

window.Alpine = Alpine;
Alpine.plugin(mask);
Alpine.start();

tippy("#home-icon", { content: "Dashboard", placement: "right" });
