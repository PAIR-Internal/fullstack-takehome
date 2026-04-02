import "@mdi/font/css/materialdesignicons.css";
import "vuetify/styles";

import { createVuetify } from "vuetify";

const pairTakehomeTheme = {
  dark: false,
  colors: {
    primary: "#171b26",
    secondary: "#4f6b92",
    background: "#f5f6fa",
    surface: "#ffffff",
    "surface-bright": "#f8f9fc",
    "surface-variant": "#ebedf4",
    error: "#d92d20",
    info: "#175cd3",
    success: "#079455",
    warning: "#dc6803",
  },
};

export default createVuetify({
  theme: {
    defaultTheme: "pairTakehomeTheme",
    themes: {
      pairTakehomeTheme,
    },
  },
  defaults: {
    VBtn: {
      rounded: "lg",
      class: "text-none",
    },
    VCard: {
      rounded: "xl",
      elevation: 0,
    },
  },
});
