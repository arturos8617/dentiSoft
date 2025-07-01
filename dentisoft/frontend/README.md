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