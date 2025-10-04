import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import tailwindcss from "@tailwindcss/vite";
import type { Plugin } from "vite";

function remoteLogger(): Plugin {
  return {
    name: "remote-logger",
    apply: "serve",
    configureServer(server) {
      const formatArg = (a: any) => {
        if (a && typeof a === "object") {
          try {
            return JSON.stringify(a);
          } catch {
            return String(a);
          }
        }
        return String(a);
      };
      server.middlewares.use("/__logs", (req, res) => {
        if (req.method !== "POST") {
          res.statusCode = 405;
          res.end("Method Not Allowed");
          return;
        }
        let data = "";
        req.on("data", (chunk) => (data += chunk));
        req.on("end", () => {
          try {
            const json = JSON.parse(data || "{}");
            const { level = "info", t, args = [] } = json || {};
            const ts = new Date(t || Date.now()).toISOString();
            const line = `[client ${ts}] ${args.map(formatArg).join(" ")}`;
            if (level === "error") console.error(line);
            else console.log(line);
          } catch (e) {
            console.error("[client-log] bad payload", e);
          }
          res.statusCode = 204;
          res.end();
        });
      });
    },
  };
}
// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), tailwindcss(), remoteLogger()],

});

