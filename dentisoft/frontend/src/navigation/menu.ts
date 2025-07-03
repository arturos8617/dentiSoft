export interface MenuItem {
    label: string;
    href: string;
    /** Roles that can see this item; empty or undefined means all roles */
    roles?: string[];
  }
  
  export const menuItems: MenuItem[] = [
    { label: "Agenda", href: "/agenda", roles: ["dentista", "CCA"] },
    { label: "Pacientes", href: "/pacientes", roles: ["dentista"] },
    { label: "Invitaciones", href: "/invitaciones/new", roles: ["CCA"] },
  ];