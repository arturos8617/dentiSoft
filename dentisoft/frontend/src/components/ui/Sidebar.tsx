import Link from "next/link";
import { menuItems } from "@/navigation/menu";

export default function Sidebar({ role }: { role?: string }) {
  const allowed = menuItems.filter(
    (item) => !item.roles || item.roles.includes(role ?? "")
  );
  return (
    <aside className="w-64 bg-[var(--color-neutral-lighter)] p-4 shadow-sm">
      <nav className="space-y-3">
        {allowed.map((item) => (
          <Link key={item.href} href={item.href}
            className="flex items-center space-x-3 rounded-md hover:bg-primary-light/10 p-2">
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
