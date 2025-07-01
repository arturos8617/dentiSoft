"use client";
import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import { getCSRFToken } from "@/lib/csrf";
import Button from "@/components/ui/Button";
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
  const [message, setMessage] = useState<
    | { text: string; type: "error" | "success" }
    | null
  >(null);

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
      setMessage({ text: "Las contraseñas no coinciden.", type: "error" });
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
      const data = await res.json();
      if (!res.ok) {
        const message =
          data.detail ||
          data.message ||
          (typeof data === "object" && data !== null
            ? Object.values(data).flat().join(" ")
            : "Error en el registro.");
        throw new Error(message);
      }
      setMessage({ text: "Registro completado con éxito.", type: "success" });
    } catch (err) {
      setMessage({
        text:
          err instanceof Error ? err.message : "Error en el registro.",
        type: "error",
      });
    }
  };

  return (
    <main className="min-h-screen bg-neutral-bg py-8 flex items-center justify-center">
      <div className="w-full max-w-xl px-4 md:px-6">
      <h1 className="text-3xl font-semibold text-neutral-800 mb-6">
          Completa tu registro
        </h1>
        <Card>
          {message && (
            <div
              className={`mb-4 text-sm text-center ${
                message.type === "error" ? "text-error" : "text-success"
              }`}
              role={message.type === "error" ? "alert" : "status"}
            >
              {message.text}
            </div>
          )}
          <form onSubmit={onSubmit} className="space-y-4">
            <input
              id="first_name"
              type="text"
              placeholder="Nombre"
              value={form.first_name}
              onChange={(e) => setForm({ ...form, first_name: e.target.value })}
              className="w-full px-4 py-3 border border-primary-subtle rounded-md"
              required
            />
            <input
              id="last_name"
              type="text"
              placeholder="Apellidos"
              value={form.last_name}
              onChange={(e) => setForm({ ...form, last_name: e.target.value })}
              className="w-full px-4 py-3 border border-primary-subtle rounded-md"
              required
            />
            <input
              id="email"
              type="email"
              value={form.email}
              readOnly
              className="w-full px-4 py-3 border border-neutral-300 rounded-md bg-neutral-lighter text-neutral-800"
            />
            <input
              id="telefono"
              type="text"
              placeholder="Teléfono"
              value={form.telefono}
              onChange={(e) => setForm({ ...form, telefono: e.target.value })}
              className="w-full px-4 py-3 border border-primary-subtle rounded-md"
              required
            />
            <input
              id="fecha_nacimiento"
              type="date"
              placeholder="Fecha de nacimiento"
              value={form.fecha_nacimiento}
              onChange={(e) =>
                setForm({ ...form, fecha_nacimiento: e.target.value })
              }
              className="w-full px-4 py-3 border border-primary-subtle rounded-md"
              required
            />
            <select
              id="genero"
              value={form.genero}
              onChange={(e) => setForm({ ...form, genero: e.target.value })}
              className="w-full px-4 py-3 border border-primary-subtle rounded-md"
              required
            >
              <option value="">Selecciona género</option>
              <option value="M">Masculino</option>
              <option value="F">Femenino</option>
              <option value="O">Otro</option>
              <option value="N">Prefiero no decir</option>
            </select>
            <input
              id="password1"
              type="password"
              placeholder="Contraseña"
              value={form.password1}
              onChange={(e) => setForm({ ...form, password1: e.target.value })}
              className="w-full px-4 py-3 border border-primary-subtle rounded-md"
              required
            />
            <input
              id="password2"
              type="password"
              placeholder="Confirmar contraseña"
              value={form.password2}
              onChange={(e) => setForm({ ...form, password2: e.target.value })}
              className="w-full px-4 py-3 border border-primary-subtle rounded-md"
              required
            />
            <div className="flex justify-end mt-6">
            <Button
                type="submit"
                className="bg-primary text-white hover:bg-primary-light"
              >
                Registrarse
              </Button>
            </div>
          </form>
        </Card>
      </div>
    </main>
  );
}