'use client';

import React, { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import Button from '@/components/ui/Button';
import FormField from '@/components/ui/FormField';
import Card from '@/components/ui/Card';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL as string;

interface Role {
  id: number;
  nombre: string;
}

interface Clinica {
  id: number;
  nombre: string;
}

const fetchRoles = async (): Promise<Role[]> => {
  const res = await fetch(`${API_BASE}/v1/roles/`);
  if (!res.ok) throw new Error('Error fetching roles');
  return res.json();
};

const fetchClinicas = async (): Promise<Clinica[]> => {
  const res = await fetch(`${API_BASE}/v1/clinicas/`);
  if (!res.ok) throw new Error('Error fetching clínicas');
  return res.json();
};

const createInvitation = async (payload: { email: string; rol: number; clinica: number }): Promise<any> => {
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
  const {
    data: rolesData,
    isLoading: rolesLoading,
    error: rolesError,
  } = useQuery<Role[], Error>({
    queryKey: ['roles'],
    queryFn: fetchRoles,
    staleTime: 5000,
    gcTime: 30000,
  });

  const roleOptions = rolesData ?? [];

  const {
    data: clinicasData,
    isLoading: clinicasLoading,
    error: clinicasError,
  } = useQuery<Clinica[], Error>({
    queryKey: ['clinicas'],
    queryFn: fetchClinicas,
    staleTime: 5000,
    gcTime: 30000,
  });

  const clinicOptions = clinicasData ?? [];

  const [email, setEmail] = useState('');
  const [rol, setRol] = useState<number | ''>('');
  const [clinica, setClinica] = useState<number | ''>('');
  const [formError, setFormError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const mutation = useMutation<any, Error, { email: string; rol: number; clinica: number }>({
    mutationFn: createInvitation,
    onSuccess: () => {
      setSuccess(true);
      setFormError(null);
    },
    onError: (err) => {
      setFormError(err.message);
      setSuccess(false);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);
    setSuccess(false);

    if (!email || !rol || !clinica) {
      setFormError('Por favor completa todos los campos.');
      return;
    }

    mutation.mutate({ email, rol: rol as number, clinica: clinica as number });
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
                  onChange={(e) => setRol(Number(e.target.value) || '')}
                  className="w-full px-4 py-3 border border-primary.subtle rounded-md focus:ring-2 focus:ring-primary.subtle"
                >
                  <option value="">Selecciona un rol...</option>
                  {roleOptions.map((r: Role) => (
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
                  onChange={(e) => setClinica(Number(e.target.value) || '')}
                  className="w-full px-4 py-3 border border-primary.subtle rounded-md focus:ring-2 focus:ring-primary.subtle"
                >
                  <option value="">Selecciona una clínica...</option>
                  {clinicOptions.map((c: Clinica) => (
                    <option key={c.id} value={c.id}>
                      {c.nombre}
                    </option>
                  ))}
                </select>
              </FormField>

              <div className="flex justify-end space-x-3 mt-6">
                <Button
                  variant="outline"
                  type="button"
                  onClick={() => {
                    setEmail('');
                    setRol('');
                    setClinica('');
                    setFormError(null);
                    setSuccess(false);
                  }}
                >
                  Cancelar
                </Button>
                <Button type="submit" disabled={mutation.isPending}>
                  {mutation.isPending ? 'Enviando...' : 'Enviar invitación'}
                </Button>
              </div>
            </form>
          )}
        </Card>
      </div>
    </main>
  );
}
