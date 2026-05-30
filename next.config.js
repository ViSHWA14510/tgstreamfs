/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    const BOT_BACKEND = process.env.BOT_BACKEND_URL || "http://localhost:8080";
    return [
      {
        source: "/api/stream/:token",
        destination: `${BOT_BACKEND}/watch/:token`,
      },
      {
        source: "/api/download/:token",
        destination: `${BOT_BACKEND}/download/:token`,
      },
    ];
  },
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          { key: "X-Frame-Options", value: "DENY" },
          { key: "X-Content-Type-Options", value: "nosniff" },
        ],
      },
    ];
  },
};

module.exports = nextConfig;
