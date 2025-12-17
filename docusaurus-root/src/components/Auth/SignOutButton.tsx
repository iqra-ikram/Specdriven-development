import React from 'react';
import { authClient } from '../../lib/auth-client';
import Translate from '@docusaurus/Translate';

export default function SignOutButton() {
  const handleLogout = async () => {
    await authClient.signOut();
    window.location.href = '/login';
  };

  return (
    <button className="button button--secondary button--sm" onClick={handleLogout}>
      <Translate id="auth.button.signout">Sign Out</Translate>
    </button>
  );
}
