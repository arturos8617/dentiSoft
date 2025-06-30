'use client';

import React, { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import Button from '@/components/ui/Button';
import FormField from '@/components/ui/FormField';
import Card from '@/components/ui/Card';
import { getCSRFToken } from '@/lib/csrf';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL as string;

interface Option {
  id: number;
  nombre: string;
}

interface InvitationPayload {
  email: string;
  rol: number;
  clinica: number;
}

const fetchRoles = async (): Promise<Option[]> => {
  const res = await fetch(`${API_BASE}/v1/roles/`, { credentials: 'include' });
  if (!res.ok) throw new Error('Error al cargar roles');
  return res.json();
};

const fetchClinicas = async (): Promise<Option[]> => {
  const res = await fetch(`${API_BASE}/v1/clinicas/`, { credentials: 'include' });
  if (!res.ok) throw new Error('Error al cargar clínicas');
  return res.json();
};

const createInvitation = async (payload: InvitationPayload) => {
  const res = await fetch(`${API_BASE}/v1/invitaciones/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCSRFToken(),
    },
    credentials: 'include',
    body: JSON.stringify(payload),
  });
  const data = await res.json();
  if (!res.ok) {
    const message =
      data.detail ||
      data.message ||
      (typeof data === 'object' && data !== null
        ? Object.values(data).flat().join(' ')
        : 'Error al crear invitación');
    throw new Error(message);
  }
  return data;
};

export default function NewInvitationPage() {
  const { data: roles, isLoading: rolesLoading } = useQuery<Option[]>({
    queryKey: ['roles'],
    queryFn: fetchRoles,
  });
  const { data: clinicas, isLoading: clinicasLoading } = useQuery<Option[]>({
    queryKey: ['clinicas'],
    queryFn: fetchClinicas,
  });

  const [form, setForm] = useState<InvitationPayload>({
    email: '',
    rol: 0,
    clinica: 0,
  });
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const mutation = useMutation({
    mutationFn: createInvitation,
    onSuccess: () => {
      setSuccess(true);
      setError(null);
      setForm({ email: '', rol: 0, clinica: 0 });
    },
    onError: (err: Error) => {
      setError(err.message);
      setSuccess(false);
    },
  });

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(false);
    if (!form.email || !form.rol || !form.clinica) {
      setError('Completa todos los campos.');
      return;
    }
    mutation.mutate(form);
  };

  if (rolesLoading || clinicasLoading) {
    return (
      <main className="min-h-screen bg-neutral.bg py-8">
        <div className="max-w-2xl mx-auto px-4 md:px-6">
          <p>Cargando...</p>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-neutral.bg py-8">
      <div className="max-w-2xl mx-auto px-4 md:px-6">
        <h1 className="text-3xl font-semibold text-neutral.800 mb-6">
          Nueva invitación
        </h1>
        <Card>
          {error && (
            <div className="mb-4 text-sm text-error.DEFAULT" role="alert">
              {error}
            </div>
          )}
          {success && (
            <div className="mb-4 text-sm text-success.DEFAULT" role="status">
              Invitación creada con éxito.
            </div>
          )}
          <form onSubmit={onSubmit} className="space-y-4">
            <FormField label="Email" htmlFor="email">
              <input
                id="email"
                type="email"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                className="w-full px-4 py-3 border border-primary.subtle rounded-md"
                required
              />
            </FormField>
            <FormField label="Rol" htmlFor="rol">
              <select
                id="rol"
                value={form.rol || ''}
                onChange={(e) => setForm({ ...form, rol: Number(e.target.value) })}
                className="w-full px-4 py-3 border border-primary.subtle rounded-md"
                required
              >
                <option value="">Selecciona</option>
                {roles?.map((r) => (
                  <option key={r.id} value={r.id}>
                    {r.nombre}
                  </option>
                ))}
              </select>
            </FormField>
            <FormField label="Clínica" htmlFor="clinica">
              <select
                id="clinica"
                value={form.clinica || ''}
                onChange={(e) => setForm({ ...form, clinica: Number(e.target.value) })}
                className="w-full px-4 py-3 border border-primary.subtle rounded-md"
                required
              >
                <option value="">Selecciona</option>
                {clinicas?.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.nombre}
                  </option>
                ))}
              </select>
            </FormField>
            <div className="flex justify-end mt-6">
              <Button type="submit" disabled={mutation.isPending}>
                {mutation.isPending ? 'Creando...' : 'Crear invitación'}
              </Button>
            </div>
          </form>
        </Card>
      </div>
    </main>
  );
}