import Alpine from "alpinejs";
import mask from "@alpinejs/mask";
import tippy from "tippy.js";

window.Alpine = Alpine;
Alpine.plugin(mask);
Alpine.start();

tippy('[data-tippy-content]', { placement: "right" });
