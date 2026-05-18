"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Bell, Menu, Search } from "lucide-react";

import { ThemeToggle } from "@/components/layout/theme-toggle";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { navigationItems } from "@/data/platform";

export function AppHeader() {
  const pathname = usePathname();
  const current = navigationItems.find((item) => (item.href === "/" ? pathname === "/" : pathname.startsWith(item.href)));

  return (
    <header className="sticky top-0 z-30 flex min-h-16 items-center gap-3 border-b bg-background/95 px-4 backdrop-blur lg:px-6">
      <Button variant="outline" size="icon" className="lg:hidden" aria-label="Open navigation">
        <Menu className="h-4 w-4" />
      </Button>
      <div className="min-w-0 flex-1">
        <div className="flex items-center gap-2">
          <h1 className="truncate text-base font-semibold">{current?.title ?? "Dashboard"}</h1>
          <Badge variant="secondary">Production</Badge>
        </div>
        <p className="hidden text-xs text-muted-foreground sm:block">AI Azure Well-Architected Review Assistant</p>
      </div>
      <div className="hidden w-full max-w-sm items-center gap-2 rounded-md border bg-card px-3 md:flex">
        <Search className="h-4 w-4 text-muted-foreground" />
        <Input className="h-9 border-0 bg-transparent px-0 shadow-none focus-visible:ring-0" placeholder="Search reviews, findings, services" />
      </div>
      <Button asChild variant="outline" size="sm" className="hidden sm:inline-flex">
        <Link href="/reports">Reports</Link>
      </Button>
      <Button variant="outline" size="icon" aria-label="Notifications">
        <Bell className="h-4 w-4" />
      </Button>
      <ThemeToggle />
      <Avatar>
        <AvatarFallback>AA</AvatarFallback>
      </Avatar>
    </header>
  );
}

