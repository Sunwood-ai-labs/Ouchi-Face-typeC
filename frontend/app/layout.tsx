import type { Metadata } from 'next';
import { ReactNode } from 'react';

import './globals.css';
import { Providers } from '../components/providers';

export const metadata: Metadata = {
  title: 'Ouchi Face',
  description: 'Self-hosted catalog for local apps, datasets, and models'
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ja" className="bg-slate-950">
      <body className="min-h-screen bg-slate-950 text-slate-100">
        <Providers>
          <div className="border-b border-slate-800 bg-slate-900/60">
            <header className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
              <span className="text-xl font-semibold tracking-wide text-primary-300">Ouchi Face</span>
              <nav className="space-x-4 text-sm font-medium text-slate-300">
                <a href="/" className="hover:text-primary-200">
                  Dashboard
                </a>
                <a href="/browse" className="hover:text-primary-200">
                  Browse
                </a>
                <a href="/admin/new" className="hover:text-primary-200">
                  Register
                </a>
              </nav>
            </header>
          </div>
          <main>{children}</main>
        </Providers>
      </body>
    </html>
  );
}
