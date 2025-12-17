import React, { useState } from 'react';
import { authClient } from '../../lib/auth-client';
import Translate from '@docusaurus/Translate';

export default function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const { data, error } = await authClient.signIn.email({
        email,
        password,
      });

      if (error) {
        setError(error.message || 'Login failed');
      } else {
        // Redirect to home/dashboard
        window.location.href = '/';
      }
    } catch (err: any) {
      setError(err.message || 'An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-form-container">
      <h2><Translate id="auth.login.title">Login</Translate></h2>
      {error && <div className="auth-error">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label><Translate id="auth.label.email">Email</Translate></label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            disabled={loading}
          />
        </div>
        <div className="form-group">
          <label><Translate id="auth.label.password">Password</Translate></label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            disabled={loading}
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? <Translate id="auth.button.loading">Logging in...</Translate> : <Translate id="auth.button.login">Login</Translate>}
        </button>
      </form>
    </div>
  );
}
