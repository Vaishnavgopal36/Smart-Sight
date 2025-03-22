// src/config.ts
export const CONFIG = {
        logoURL: "/logo.png", // Public assets should be accessed without "/public/"
        siteTitle: "SmartSight",
      };

export const API_BASE_URL =
  import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";
