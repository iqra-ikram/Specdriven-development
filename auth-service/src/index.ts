import { Hono } from "hono";
import { auth } from "./auth";
import { serve } from "@hono/node-server";
import { cors } from "hono/cors";

const app = new Hono();

app.use(
  "/api/*",
  cors({
    origin: ["http://localhost:3000"],
    allowMethods: ["POST", "GET", "OPTIONS"],
    allowHeaders: ["Content-Type", "Authorization"],
    exposeHeaders: ["Content-Length"],
    maxAge: 600,
    credentials: true,
  })
);

app.on(["POST", "GET"], "/api/auth/*", (c) => {
  return auth.handler(c.req.raw);
});

const port = 4000;
console.log(`Server is running on port ${port}`);

serve({
  fetch: app.fetch,
  port,
});
