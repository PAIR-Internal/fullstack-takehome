import { createPinia } from "pinia";
import { createApp } from "vue";

import App from "./App.vue";

import { router } from "@/router";
import vuetify from "@/plugins/vuetify";

import "@/styles/theme.scss";

createApp(App).use(createPinia()).use(vuetify).use(router).mount("#app");
