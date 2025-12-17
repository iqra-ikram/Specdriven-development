import React from 'react';
import { Redirect } from '@docusaurus/router';
import { authClient } from '../../lib/auth-client';

export default function RequireAuth({ children }: { children: JSX.Element }) {
  const { data: session, isPending, error } = authClient.useSession();

  if (isPending) {
    return <div>Loading...</div>; // TODO: Replace with proper loading spinner
  }

  if (error || !session) {
    return <Redirect to="/login" />;
  }

  return children;
}
