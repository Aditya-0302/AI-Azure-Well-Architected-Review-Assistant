"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { CloudCog } from "lucide-react";

import { navigationItems } from "@/data/platform";
import { cn } from "@/lib/utils";

export function AppSidebar() {
  const pathname = usePathname();

  return (
    <aside className="hidden w-72 shrink-0 border-r bg-card lg:flex lg:flex-col">
      <div className="flex h-16 items-center gap-3 border-b px-5">
        <div className="flex h-9 w-9 items-center justify-center rounded-md bg-primary text-primary-foreground">
          <CloudCog className="h-5 w-5" />
        </div>
        <div className="min-w-0">
          <p className="truncate text-sm font-semibold">Azure WAF Assistant</p>
          <p className="truncate text-xs text-muted-foreground">Enterprise review console</p>
        </div>
      </div>
      <nav className="flex flex-1 flex-col gap-1 p-3">
        {navigationItems.map((item) => {
          const active = item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex h-10 items-center gap-3 rounded-md px-3 text-sm font-medium text-muted-foreground transition-colors hover:bg-muted hover:text-foreground",
                active && "bg-primary/10 text-primary"
              )}
            >
              <Icon className="h-4 w-4" />
              {item.title}
            </Link>
          );
        })}
      </nav>
      <div className="border-t p-4">
        <div className="rounded-md border bg-muted/35 p-3">
          <p className="text-xs font-semibold text-foreground">Tenant</p>
          <p className="mt-1 text-sm text-muted-foreground">Contoso Enterprise Cloud</p>
        </div>
      </div>
    </aside>
  );
}

