import React from 'react';
import { authClient } from '../../lib/auth-client';
import Link from '@docusaurus/Link';
import SignOutButton from '../../components/Auth/SignOutButton';

export default function AuthNavbarItem() {
  const { data: session, isPending, error } = authClient.useSession();

  // If we have a session, show user info
  if (session) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <span>Hi, {session.user.name}</span>
        <SignOutButton />
      </div>
    );
  }

  // Default: Show Login/Signup buttons (even if pending/error, to ensure they are visible)
  // You might want a spinner for 'isPending', but for now let's ensure visibility.
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
      <Link to="/login" className="button button--primary button--sm">Login</Link>
      <Link to="/signup" className="button button--secondary button--sm">Sign Up</Link>
    </div>
  );
}
