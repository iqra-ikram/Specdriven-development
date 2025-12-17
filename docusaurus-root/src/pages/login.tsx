import React from 'react';
import Layout from '@theme/Layout';
import LoginForm from '../components/Auth/LoginForm';
import Translate from '@docusaurus/Translate';

export default function Login() {
  return (
    <Layout title="Login" description="Login to your account">
      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          height: '50vh',
          fontSize: '20px',
        }}>
        <LoginForm />
      </div>
    </Layout>
  );
}
