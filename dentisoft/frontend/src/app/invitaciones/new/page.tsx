'use client';

import React, { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import AppLayout from '@/components/ui/AppLayout';
import Button from '@/components/ui/Button';
import Card from '@/components/ui/Card';
import FormField from '@/components/ui/FormField';
import { getCSRFToken } from '@/utils/csrf';

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
  const [message, setMessage] = useState<
    | { text: string; type: "error" | "success" }
    | null
     >(null);

    const mutation = useMutation({
      mutationFn: createInvitation,
      onSuccess: () => {
        setMessage({ text: 'Invitación creada con éxito.', type: 'success' });
        setForm({ email: '', rol: 0, clinica: 0 });
      },
      onError: (err: Error) => {
        setMessage({ text: err.message, type: 'error' });
      },
    });
  
    const onSubmit = (e: React.FormEvent) => {
      e.preventDefault();
      setMessage(null);
      if (!form.email || !form.rol || !form.clinica) {
        setMessage({ text: 'Completa todos los campos.', type: 'error' });
        return;
      }
      mutation.mutate(form);
    };
  
    if (rolesLoading || clinicasLoading) {
      return (
        <AppLayout title="Nueva invitación">
          <p>Cargando...</p>
        </AppLayout>
      );
    }
    
    return (
      <AppLayout title="Nueva invitación">
        <div className="mx-auto max-w-xl p-[var(--space-6)]">
          <Card>
            <h2 className="mb-4 text-xl font-heading text-[var(--color-neutral-800)]">
              Invitar usuario
            </h2>
            {message && (
              <div
                className={`mb-4 text-sm font-medium ${
                  message.type === 'error'
                    ? 'text-[var(--color-error)]'
                    : 'text-[var(--color-success)]'
                }`}
                role={message.type === 'error' ? 'alert' : 'status'}
              >
                {message.text}
              </div>
            )}
            <form onSubmit={onSubmit} className="space-y-[var(--space-4)]">
              <FormField label="Email" htmlFor="email">
                <input
                  id="email"
                  type="email"
                  value={form.email}
                  onChange={(e) => setForm({ ...form, email: e.target.value })}
                  required
                />
              </FormField>
              <FormField label="Rol" htmlFor="rol">
                <select
                  id="rol"
                  value={form.rol || ''}
                  onChange={(e) => setForm({ ...form, rol: Number(e.target.value) })}
                  required
                >
                  <option value="">Selecciona rol</option>
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
                  required
                >
                  <option value="">Selecciona clínica</option>
                  {clinicas?.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.nombre}
                    </option>
                  ))}
                </select>
              </FormField>
  
              <div className="flex justify-end mt-[var(--space-6)]">
                <Button type="submit" className="w-full" disabled={mutation.isPending}>
                  {mutation.isPending ? 'Creando...' : 'Enviar invitación'}
                </Button>
              </div>
            </form>
          </Card>
        </div>
      </AppLayout>
    );
    }