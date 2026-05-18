import type { Metadata } from "next";
import type * as React from "react";

import { AppShell } from "@/components/layout/app-shell";
import { ThemeProvider } from "@/components/theme-provider";
import "@/app/globals.css";

export const metadata: Metadata = {
  title: "AI Azure Well-Architected Review Assistant",
  description: "Enterprise Azure Well-Architected review automation platform"
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider>
          <AppShell>{children}</AppShell>
        </ThemeProvider>
      </body>
    </html>
  );
}
