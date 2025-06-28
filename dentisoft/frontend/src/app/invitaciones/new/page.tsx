'use client';

import React, { useState } from 'react';
import { useParams } from 'next/navigation';
import { useQuery, useMutation } from '@tanstack/react-query';
import Button from '@/components/ui/Button';
import FormField from '@/components/ui/FormField';
import Card from '@/components/ui/Card';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL as string;
// El endpoint de registro de invitación no está bajo /v1
const REGISTER_URL = API_BASE.replace(/\/api$/, '') + '/api/invite-register/';

interface Invitation {
  id: number;
  email: string;
  rol: number;
  clinica: number;
  estado: string;
}

interface RegisterPayload {
  token: string;
  name: string;
  email: string;
  password: string;
}

const fetchInvitation = async (token: string): Promise<Invitation | null> => {
  const res = await fetch(`${API_BASE}/v1/invitaciones/?token=${token}`, { credentials: 'include' });
  if (!res.ok) throw new Error('Error fetching invitation');
  const data = (await res.json()) as Invitation[];
  return data.length > 0 ? data[0] : null;
};

const registerFromInvitation = async (payload: RegisterPayload): Promise<any> => {
  const res = await fetch(REGISTER_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(payload),
  });
  const data = await res.json();
  if (!res.ok) {
    const message = data.detail || data.message || 'Error registering user';
    throw new Error(message);
  }
  return data;
};

export default function AcceptInvitationPage() {
  const { token } = useParams() as { token: string };
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const [formError, setFormError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const { data: invitation, isLoading, error } = useQuery<Invitation | null, Error>([
    'invitation',
    token
  ], () => fetchInvitation(token), { enabled: !!token });

  const mutation = useMutation<any, Error, RegisterPayload>(registerFromInvitation, {
    onSuccess: () => {
      setSuccess(true);
      setFormError(null);
    },
    onError: (err) => {
      setFormError(err.message);
      setSuccess(false);
    }
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);
    setSuccess(false);

    if (!invitation || !name || !password) {
      setFormError('Por favor completa todos los campos.');
      return;
    }
    mutation.mutate({ token, name, email: invitation.email, password });
  };

  // Estados de carga o error inicial
  if (isLoading) {
    return (
      <main className="min-h-screen bg-neutral.bg py-8">
        <div className="max-w-2xl mx-auto px-4 md:px-6">
          <p>Cargando invitación...</p>
        </div>
      </main>
    );
  }

  if (error || !invitation) {
    return (
      <main className="min-h-screen bg-neutral.bg py-8">
        <div className="max-w-2xl mx-auto px-4 md:px-6">
          <p className="text-error.DEFAULT text-center">Invitación inválida o expirada.</p>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-neutral.bg py-8">
      <div className="max-w-2xl mx-auto px-4 md:px-6">
        <h1 className="text-3xl font-semibold text-neutral.800 mb-6">
          Completa tu registro
        </h1>

        <Card>
          {formError && (
            <div className="mb-4 text-sm text-error.DEFAULT" role="alert">
              {formError}
            </div>
          )}
          {success && (
            <div className="mb-4 text-sm text-success.DEFAULT" role="status">
              Registro completado con éxito.
            </div>
          )}

          <form onSubmit={handleSubmit} noValidate>
            <FormField label="Email" htmlFor="email">
              <input
                id="email"
                type="email"
                value={invitation.email}
                readOnly
                className="w-full px-4 py-3 border border-neutral.300 rounded-md bg-neutral.lighter text-neutral.800"
              />
            </FormField>

            <FormField label="Nombre completo" htmlFor="name">
              <input
                id="name"
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full px-4 py-3 border border-primary.subtle rounded-md focus:ring-2 focus:ring-primary.subtle"
              />
            </FormField>

            <FormField label="Contraseña" htmlFor="password">
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 border border-primary.subtle rounded-md focus:ring-2 focus:ring-primary.subtle"
              />
            </FormField>

            <div className="flex justify-end space-x-3 mt-6">
              <Button
                variant="outline"
                type="button"
                onClick={() => {
                  setName('');
                  setPassword('');
                  setFormError(null);
                  setSuccess(false);
                }}
              >
                Cancelar
              </Button>
              <Button type="submit" disabled={mutation.isPending}>
                {mutation.isPending ? 'Registrando...' : 'Registrar'}
              </Button>
            </div>
          </form>
        </Card>
      </div>
    </main>
  );
}
