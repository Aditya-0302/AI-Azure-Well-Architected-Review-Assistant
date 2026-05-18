"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { navigationItems } from "@/data/platform";
import { cn } from "@/lib/utils";

export function MobileNav() {
  const pathname = usePathname();
  const visibleItems = navigationItems.slice(0, 5);

  return (
    <nav className="fixed inset-x-0 bottom-0 z-40 border-t bg-card px-2 py-2 lg:hidden">
      <div className="grid grid-cols-5 gap-1">
        {visibleItems.map((item) => {
          const active = item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex h-12 flex-col items-center justify-center gap-1 rounded-md text-[11px] font-medium text-muted-foreground",
                active && "bg-primary/10 text-primary"
              )}
            >
              <Icon className="h-4 w-4" />
              <span className="truncate">{item.title}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}

