"use client";
import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import { getCSRFToken } from "@/lib/csrf";
import Button from "@/components/ui/Button";
import FormField from "@/components/ui/FormField";
import Card from "@/components/ui/Card";

export default function AcceptInvitationPage() {
  const { token } = useParams();
  const [valid, setValid] = useState<boolean | null>(null);
  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    email: "",
    telefono: "",
    fecha_nacimiento: "",
    genero: "",
    password1: "",
    password2: "",
  });
  const [msg, setMsg] = useState<string | null>(null);

  useEffect(() => {
    if (!token) return;
    fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/v1/invitaciones/?token=${token}`,
      {
        credentials: "include",
      }
    )
      .then((res) => {
        if (!res.ok) throw new Error();
        return res.json();
      })
      .then((data) => {
        setForm((f) => ({ ...f, email: data[0].email }));
        setValid(true);
      })
      .catch(() => setValid(false));
  }, [token]);

  if (valid === null) return <p className="text-center">Validando...</p>;
  if (!valid)
    return (
      <p className="text-center text-red-600">
        Invitación inválida o expirada.
      </p>
    );

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (form.password1 !== form.password2) {
      setMsg("Las contraseñas no coinciden.");
      return;
    }
    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_BASE_URL}/invite-register/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
          },
          credentials: "include",
          body: JSON.stringify({ token, ...form }),
        }
      );
      if (!res.ok) throw new Error();
      setMsg("Registro completado con éxito.");
    } catch {
      setMsg("Error en el registro.");
    }
  };

  return (
    <main className="min-h-screen bg-neutral.bg py-8">
      <div className="max-w-xl mx-auto px-4 md:px-6">
        <h1 className="text-3xl font-semibold text-neutral.800 mb-6">
          Completa tu registro
        </h1>
        <Card>
          {msg && <p className="mb-4 text-center">{msg}</p>}
          <form onSubmit={onSubmit} className="space-y-4">
            <FormField label="Nombre" htmlFor="first_name">
              <input
                id="first_name"
                type="text"
                value={form.first_name}
                onChange={(e) =>
                  setForm({ ...form, first_name: e.target.value })
                }
                className="w-full px-4 py-3 border border-primary.subtle rounded-md"
                required
              />
            </FormField>
            <FormField label="Apellidos" htmlFor="last_name">
              <input
                id="last_name"
                type="text"
                value={form.last_name}
                onChange={(e) =>
                  setForm({ ...form, last_name: e.target.value })
                }
                className="w-full px-4 py-3 border border-primary.subtle rounded-md"
                required
              />
            </FormField>
            <FormField label="Correo" htmlFor="email">
              <input
                id="email"
                type="email"
                value={form.email}
                readOnly
                className="w-full px-4 py-3 border border-neutral.300 rounded-md bg-neutral.lighter text-neutral.800"
              />
            </FormField>
            <FormField label="Teléfono" htmlFor="telefono">
              <input
                id="telefono"
                type="text"
                value={form.telefono}
                onChange={(e) =>
                  setForm({ ...form, telefono: e.target.value })
                }
                className="w-full px-4 py-3 border border-primary.subtle rounded-md"
                required
              />
            </FormField>
            <FormField label="Fecha de nacimiento" htmlFor="fecha_nacimiento">
              <input
                id="fecha_nacimiento"
                type="date"
                value={form.fecha_nacimiento}
                onChange={(e) =>
                  setForm({ ...form, fecha_nacimiento: e.target.value })
                }
                className="w-full px-4 py-3 border border-primary.subtle rounded-md"
                required
              />
            </FormField>
            <FormField label="Género" htmlFor="genero">
              <select
                id="genero"
                value={form.genero}
                onChange={(e) =>
                  setForm({ ...form, genero: e.target.value })
                }
                className="w-full px-4 py-3 border border-primary.subtle rounded-md"
                required
              >
                <option value="">Selecciona</option>
                <option value="M">Masculino</option>
                <option value="F">Femenino</option>
                <option value="O">Otro</option>
                <option value="N">Prefiero no decir</option>
              </select>
            </FormField>
            <FormField label="Contraseña" htmlFor="password1">
              <input
                id="password1"
                type="password"
                value={form.password1}
                onChange={(e) =>
                  setForm({ ...form, password1: e.target.value })
                }
                className="w-full px-4 py-3 border border-primary.subtle rounded-md"
                required
              />
            </FormField>
            <FormField label="Confirmar contraseña" htmlFor="password2">
              <input
                id="password2"
                type="password"
                value={form.password2}
                onChange={(e) =>
                  setForm({ ...form, password2: e.target.value })
                }
                className="w-full px-4 py-3 border border-primary.subtle rounded-md"
                required
              />
            </FormField>
            <div className="flex justify-end mt-6">
              <Button type="submit">Registrar</Button>
            </div>
          </form>
        </Card>
      </div>
    </main>
  );
}