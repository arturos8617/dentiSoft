'use client';

import React, { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import Button from '@/components/ui/Button';
import FormField from '@/components/ui/FormField';
import Card from '@/components/ui/Card';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL;

// Fetch roles and clinicas
const fetchRoles = async () => {
  const res = await fetch(`${API_BASE}/v1/roles/`);
  if (!res.ok) throw new Error('Error fetching roles');
  return res.json() as Promise<{ id: number; nombre: string }[]>;
};
const fetchClinicas = async () => {
  const res = await fetch(`${API_BASE}/v1/clinicas/`);
  if (!res.ok) throw new Error('Error fetching clínicas');
  return res.json() as Promise<{ id: number; nombre: string }[]>;
};

// Create invitation
const createInvitation = async (payload: { email: string; rol: number; clinica: number }) => {
  const res = await fetch(`${API_BASE}/v1/invitaciones/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  const data = await res.json();
  if (!res.ok) {
    const message = data.detail || data.message || 'Error creating invitation';
    throw new Error(message);
  }
  return data;
};

export default function NewInvitationPage() {
  const { data: roles, isLoading: rolesLoading, error: rolesError } = useQuery(['roles'], fetchRoles);
  const { data: clinicas, isLoading: clinicasLoading, error: clinicasError } = useQuery(
    ['clinicas'],
    fetchClinicas
  );

  const [email, setEmail] = useState('');
  const [rol, setRol] = useState('');
  const [clinica, setClinica] = useState('');
  const [formError, setFormError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const mutation = useMutation(createInvitation, {
    onSuccess: () => {
      setSuccess(true);
      setFormError(null);
    },
    onError: (err: any) => {
      setFormError(err.message);
      setSuccess(false);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);
    setSuccess(false);

    // Basic validation
    if (!email || !rol || !clinica) {
      setFormError('Por favor completa todos los campos.');
      return;
    }

    mutation.mutate({
      email,
      rol: parseInt(rol, 10),
      clinica: parseInt(clinica, 10),
    });
  };

  return (
    <main className="min-h-screen bg-neutral.bg py-8">
      <div className="max-w-4xl mx-auto px-4 md:px-6">
        <h1 className="text-3xl font-semibold text-neutral.800 mb-6">
          Invitar nuevo usuario
        </h1>

        <Card>
          {rolesLoading || clinicasLoading ? (
            <p>Cargando datos...</p>
          ) : rolesError || clinicasError ? (
            <p className="text-error.DEFAULT">Error cargando datos.</p>
          ) : (
            <form onSubmit={handleSubmit} noValidate>
              {formError && (
                <div className="mb-4 text-sm text-error.DEFAULT" role="alert">
                  {formError}
                </div>
              )}
              {success && (
                <div className="mb-4 text-sm text-success.DEFAULT" role="status">
                  Invitación enviada con éxito.
                </div>
              )}

              <FormField label="Email o teléfono" htmlFor="email">
                <input
                  id="email"
                  type="text"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-4 py-3 border border-primary.subtle rounded-md focus:ring-2 focus:ring-primary.subtle"
                />
              </FormField>

              <FormField label="Rol" htmlFor="rol">
                <select
                  id="rol"
                  value={rol}
                  onChange={(e) => setRol(e.target.value)}
                  className="w-full px-4 py-3 border border-primary.subtle rounded-md focus:ring-2 focus:ring-primary.subtle"
                >
                  <option value="">Selecciona un rol...</option>
                  {roles!.map((r) => (
                    <option key={r.id} value={r.id}>
                      {r.nombre}
                    </option>
                  ))}
                </select>
              </FormField>

              <FormField label="Clínica" htmlFor="clinica">
                <select
                  id="clinica"
                  value={clinica}
                  onChange={(e) => setClinica(e.target.value)}
                  className="w-full px-4 py-3 border border-primary.subtle rounded-md focus:ring-2 focus:ring-primary.subtle"
                >
                  <option value="">Selecciona una clínica...</option>
                  {clinicas!.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.nombre}
                    </option>
                  ))}
                </select>
              </FormField>

              <div className="flex justify-end space-x-3 mt-6">
                <Button variant="outline" type="button" onClick={() => {
                  setEmail(''); setRol(''); setClinica(''); setFormError(null); setSuccess(false);
                }}>
                  Cancelar
                </Button>
                <Button type="submit" disabled={mutation.isLoading}>
                  {mutation.isLoading ? 'Enviando...' : 'Enviar invitación'}
                </Button>
              </div>
            </form>
          )}
        </Card>
      </div>
    </main>
  );
}
