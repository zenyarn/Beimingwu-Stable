import { createApp } from "vue";
import "./style.css";
import router from "./router";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
import store from "./store";
import i18n from "./i18n";

// windicss
import "virtual:windi.css";

createApp(App).use(vuetify).use(router).use(store).use(i18n).mount("#app");
