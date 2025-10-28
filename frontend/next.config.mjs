/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  experimental: {
    serverActions: true
  },
  images: {
    remotePatterns: [
      {
        protocol: 'http',
        hostname: '**'
      },
      {
        protocol: 'https',
        hostname: '**'
      }
    ]
  }
};

export default nextConfig;
