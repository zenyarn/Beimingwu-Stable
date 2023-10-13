import { defineConfig } from "vitepress";
import mathjax3 from "markdown-it-mathjax3";
import { customElement } from "./mathjax";
import { LocaleConfig } from "vitepress";
import locales from "./locales";

export default defineConfig({
  title: " ",
  description: "A VitePress Site",
  locales: locales as LocaleConfig,
  markdown: {
    config: (md) => {
      md.use(mathjax3);
    },
  },
  vue: {
    template: {
      compilerOptions: {
        isCustomElement: (tag) => customElement.includes(tag),
      },
    },
  },

  head: [
    [
      "link",
      {
        rel: "stylesheet",
        href: "https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.5.1/katex.min.css",
        crossorigin: "",
      },
    ],
  ],
});
