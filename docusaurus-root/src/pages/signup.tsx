import React from 'react';
import Layout from '@theme/Layout';
import SignUpForm from '../components/Auth/SignUpForm';
import Translate from '@docusaurus/Translate';

export default function SignUp() {
  return (
    <Layout title="Sign Up" description="Create a new account">
      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          height: '50vh',
          fontSize: '20px',
        }}>
        <SignUpForm />
      </div>
    </Layout>
  );
}
