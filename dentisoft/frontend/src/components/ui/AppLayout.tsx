import React from "react";

export interface AppLayoutProps {
  /** Page title displayed in the header */
  title: string;
  /** Main content */
  children: React.ReactNode;
}

/**
 * Global application layout using the design tokens defined in globals.css.
 */
export const AppLayout: React.FC<AppLayoutProps> = ({ title, children }) => {
  return (
    <div className="flex min-h-screen bg-[var(--color-neutral-bg)]">
      <aside className="w-64 bg-[var(--color-neutral-lighter)] p-4 shadow-sm">
        {/* Sidebar items */}
      </aside>
      <div className="flex-1 flex flex-col">
        <header className="h-16 bg-[var(--color-neutral-lighter) shadow-sm flex items-center px-6">
          <h1 className="text-2xl font-heading text-[var(--color-neutral-800)]">
            {title}
          </h1>
        </header>
        <main className="flex-1 overflow-auto p-6">{children}</main>
      </div>
    </div>
  );
};

export default AppLayout;
