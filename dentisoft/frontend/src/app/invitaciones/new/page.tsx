"use client";
import { useState } from "react";

export default function NewInvitationPage() {
  const [email, setEmail] = useState("");
  const [rol, setRol] = useState("");
  const [clinica, setClinica] = useState("");
  const [msg, setMsg] = useState<string | null>(null);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_BASE_URL}/v1/invitaciones/`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, rol: +rol, clinica: +clinica }),
        }
      );
      if (!res.ok) throw new Error();
      setMsg("Invitación enviada con éxito.");
      setEmail("");
      setRol("");
      setClinica("");
    } catch {
      setMsg("Error al enviar la invitación.");
    }
  };

  return (
    <div className="max-w-lg mx-auto p-6">
      <h1 className="text-2xl font-semibold mb-4">Invitar Usuario</h1>
      {msg && <p className="mb-4 text-center">{msg}</p>}
      <form onSubmit={onSubmit} className="space-y-4">
        <input
          type="email"
          placeholder="Correo electrónico"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full p-2 border rounded"
          required
        />
        <input
          type="number"
          placeholder="Rol (ID)"
          value={rol}
          onChange={(e) => setRol(e.target.value)}
          className="w-full p-2 border rounded"
          required
        />
        <input
          type="number"
          placeholder="Clínica (ID)"
          value={clinica}
          onChange={(e) => setClinica(e.target.value)}
          className="w-full p-2 border rounded"
          required
        />
        <button
          type="submit"
          className="w-full py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Enviar Invitación
        </button>
      </form>
    </div>
  );
}
