This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.

## Colores (HEX)
| Token             | Uso                                  | Valor HEX |
| ----------------- | ------------------------------------ | --------- |
| `primary.DEFAULT` | Botones principales, enlaces activos | `#4773A1` |
| `primary.light`   | Hover / focus                        | `#6A90B4` |
| `primary.lighter` | Fondos de estado, acentos suaves     | `#8DADC7` |
| `primary.subtle`  | Borde de inputs, focus ring          | `#B1CADA` |
| `neutral.bg`      | Fondo de página                      | `#FCFCFC` |
| `neutral.lighter` | Fondos de cards read-only/empty      | `#F9FAFB` |
| `neutral.800`     | Texto principal                      | `#1F2937` |
| `error.DEFAULT`   | Errores (texto, íconos)              | `#DC2626` |
| `success.DEFAULT` | Éxito (texto, íconos)                | `#16A34A` |
| `warning.DEFAULT` | Advertencias                         | `#D97706` |
| `info.DEFAULT`    | Mensajes informativos                | `#0EA5E9` |


## Tipografía

### Familias

- **Cuerpo y UI:** `Inter`, `sans-serif`
- **Títulos y branding:** `Rubik`, `sans-serif`

### Escala de tamaños

| Token | Tamaño     | Line-height |
| ----- | ---------- | ----------- |
| `sm`  | `0.875rem` | `1.25rem`   |
| `base`| `1rem`     | `1.5rem`    |
| `lg`  | `1.125rem` | `1.75rem`   |
| `xl`  | `1.25rem`  | `1.75rem`   |
| `2xl` | `1.5rem`   | `2rem`      |
| `3xl` | `1.875rem` | `2.25rem`   |
| `4xl` | `2.25rem`  | `2.5rem`    |

Estas fuentes y tamaños también están configurados en `tailwind.config.js` y
expuestos como variables CSS en `src/app/globals.css` para su uso directo.



## Escala de espaciado

| Token | Valor  | Uso típico                                  |
| ----- | ------ | -----------------------------------------   |       
| `1`   | `4px`  | Gaps muy pequeños (iconos, badges)          |
| `2`   | `8px`  | Gaps entre elementos muy juntos             |
| `3`   | `12px` | Padding pequeño en inputs                   |
| `4`   | `16px` | Margen estándar entre campos y secciones    |
| `6`   | `24px` | Separación media en cards                   |
| `8`   | `32px` | Padding/layout principal                    |
| `10`  | `40px` | Separación generosa en hero sections        |
| `12`  | `48px` | Márgenes grandes en layout                  |
| `16`  | `64px` | Grandes espacios en pantallas de bienvenida |

Estos valores están definidos en `tailwind.config.js` y disponibles como variables CSS en `src/app/globals.css` para que puedas utilizarlos en cualquier parte de tu aplicación.



## Bordes y Sombras

### Border-Radius

| Token | Valor | Uso típico |
| ----- | ----- | ---------- |
| `sm` | `0.25rem` (4px) | Esquinas sutiles |
| `md` | `0.5rem` (8px) | Contenedores generales |
| `lg` | `0.75rem` (12px) | Modales u overlays |
| `full` | `9999px` | Avatares y badges |

### Box-Shadow

| Token | Valor | Uso típico |
| ----- | -------------------------------------------------------- | ------------------- |
| `sm` | `0 1px 2px rgba(0,0,0,0.05)`                              | Encabezados, inputs |
| `md` | `0 4px 6px rgba(0,0,0,0.1), 0 2px 4px rgba(0,0,0,0.06)`   | Cards               |
| `lg` | `0 10px 15px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.05)` | Modales y overlays  |
| `inner` | `inset 0 2px 4px rgba(0,0,0,0.06)`                     | Inputs enfocados internamente |

Estos valores también provienen de `tailwind.config.js` y están expuestos como variables CSS en `src/app/globals.css`.

### Íconos clave

| Componente | Uso |
| ---------- | --------------------------------------------------- |
| `UserPlusIcon` | Invitar usuarios |
| `EnvelopeIcon` | Correo |
| `CalendarIcon` | Fecha |
| `PhoneIcon` | Teléfono |
| `LockClosedIcon` | Contraseña |
| `CheckCircleIcon` / `XCircleIcon` | Éxito / Error |

Puedes importarlos directamente desde `src/components/ui/Icons.tsx`.



## Global Layout Blueprint

To maintain consistency across pages, a base layout component can be used. It leverages the design tokens defined in `globals.css`:

```tsx
import AppLayout from './src/components/AppLayout';

<AppLayout title="Título pantalla">
  {/* Page content here */}
</AppLayout>
```

`AppLayout` renders the following structure:

```html
<div class="flex min-h-screen bg-[var(--color-neutral-bg)]">
  <aside class="w-64 bg-[var(--color-neutral-lighter)] p-4 shadow-sm">
    <!-- Sidebar items -->
  </aside>
  <div class="flex-1 flex flex-col">
    <header class="h-16 bg-white shadow-sm flex items-center px-6">
      <h1 class="text-2xl font-heading text-[var(--color-neutral-800)]">
        Título pantalla
      </h1>
    </header>
    <main class="flex-1 overflow-auto p-6">
      <!-- Page content -->
    </main>
  </div>
</div>
```

This blueprint ensures the sidebar, header and main content areas share the same styling tokens across the project.