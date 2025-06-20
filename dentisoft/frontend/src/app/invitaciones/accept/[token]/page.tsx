"use client";
import { useState, useEffect } from "react";
import { useParams } from "next/navigation";

export default function AcceptInvitationPage() {
  const { token } = useParams();
  const [valid, setValid] = useState<boolean | null>(null);
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [msg, setMsg] = useState<string | null>(null);

  useEffect(() => {
    if (!token) return;
    fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/v1/invitaciones/?token=${token}`
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
    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_BASE_URL}/invite-register/`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
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
    <div className="max-w-lg mx-auto p-6">
      <h1 className="text-2xl font-semibold mb-4">
        Completa tu Registro
      </h1>
      {msg && <p className="mb-4 text-center">{msg}</p>}
      <form onSubmit={onSubmit} className="space-y-4">
        <input
          type="text"
          placeholder="Nombre completo"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
          className="w-full p-2 border rounded"
          required
        />
        <input
          type="email"
          placeholder="Correo electrónico"
          value={form.email}
          readOnly
          className="w-full p-2 border rounded bg-gray-100"
        />
        <input
          type="password"
          placeholder="Contraseña"
          value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
          className="w-full p-2 border rounded"
          required
        />
        <button
          type="submit"
          className="w-full py-2 bg-green-600 text-white rounded hover:bg-green-700"
        >
          Registrar
        </button>
      </form>
    </div>
  );
}
