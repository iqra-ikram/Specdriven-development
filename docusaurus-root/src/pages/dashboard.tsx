import React from 'react';
import Layout from '@theme/Layout';
import RequireAuth from '../components/Auth/RequireAuth';
import { authClient } from '../lib/auth-client';

function DashboardContent() {
  const { data: session } = authClient.useSession();

  return (
    <div className="container margin-vert--xl">
      <h1>Welcome, {session?.user?.name}!</h1>
      <p>This is a protected dashboard.</p>
      <p>Email: {session?.user?.email}</p>
      {/* Future: Add list of AI agents or robots here */}
    </div>
  );
}

export default function Dashboard() {
  return (
    <Layout title="Dashboard">
      <RequireAuth>
        <DashboardContent />
      </RequireAuth>
    </Layout>
  );
}
