import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { AuthProvider } from '@/contexts/AuthContext';

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => jest.fn(),
}));

jest.mock('@/components/Sidebar', () => () => <div />);
jest.mock('@/components/Menubar', () => () => <div />);

const api = jest.mock('@/lib/api', () => ({
  fetchCurrentUser: jest.fn(),
  updateUserProfile: jest.fn(),
  resolveMediaUrl: (p: string) => p,
}));

// Helper to set tokens for auth guard
function setTokens() {
  localStorage.setItem('authTokens', JSON.stringify({ access: 'test', refresh: 'x' }));
}

function setAuthUser(user: Record<string, any>) {
  localStorage.setItem('authUser', JSON.stringify(user));
}

describe('Profile Page', () => {
  beforeEach(() => {
    localStorage.clear();
    jest.clearAllMocks();
  });

  it('shows skeletons while loading', async () => {
    setTokens();
    const { fetchCurrentUser } = require('@/lib/api');
    (fetchCurrentUser as jest.Mock).mockResolvedValueOnce({});

    const Profile = require('../Profile').default;
    render(
      <AuthProvider>
        <Profile />
      </AuthProvider>
    );

    const skeletons = document.querySelectorAll('[data-slot="skeleton"]');
    expect(skeletons.length).toBeGreaterThan(0);
  });

  it('loads and populates user data', async () => {
    setTokens();
    setAuthUser({
      full_name: 'Jane Doe',
      mobile_number: '9999999999',
      email: 'jane@example.com',
      profile: { state: 'Bihar', district: 'Patna', pincode: '800001', current_class: 'BCECE', village: 'Kankarbagh' }
    });

    const Profile = require('../Profile').default;
    render(
      <AuthProvider>
        <Profile />
      </AuthProvider>
    );

    await waitFor(() => {
      expect(screen.getByLabelText(/Full Name/i)).toHaveValue('Jane Doe');
    });
    expect(screen.getByLabelText(/Phone Number/i)).toHaveValue('9999999999');
    expect(screen.getByLabelText(/Email Address/i)).toHaveValue('jane@example.com');
  });

  it('validates inputs and prevents save when invalid', async () => {
    setTokens();
    setAuthUser({ full_name: 'John Doe', mobile_number: '8888888888', email: 'john@example.com' });
    const { updateUserProfile } = require('@/lib/api');

    const Profile = require('../Profile').default;
    render(
      <AuthProvider>
        <Profile />
      </AuthProvider>
    );

    // Enter edit mode
    const editBtn = await screen.findByRole('button', { name: /Edit Profile/i });
    fireEvent.click(editBtn);

    const phoneInput = screen.getByLabelText(/Phone Number/i);
    const emailInput = screen.getByLabelText(/Email Address/i);

    fireEvent.change(phoneInput, { target: { value: '123' } });
    fireEvent.change(emailInput, { target: { value: 'bad-email' } });

    const saveBtn = screen.getByRole('button', { name: /Save/i });
    fireEvent.click(saveBtn);

    expect(updateUserProfile).not.toHaveBeenCalled();
    expect(await screen.findByText(/Phone must be 10 digits/i)).toBeInTheDocument();
  });

  it('submits valid payload and refreshes user', async () => {
    setTokens();
    setAuthUser({ full_name: 'Test User', mobile_number: '7777777777' });
    const { updateUserProfile } = require('@/lib/api');
    (updateUserProfile as jest.Mock).mockResolvedValueOnce({ data: { ok: true } });

    const Profile = require('../Profile').default;
    render(
      <AuthProvider>
        <Profile />
      </AuthProvider>
    );

    const editBtn = await screen.findByRole('button', { name: /Edit Profile/i });
    fireEvent.click(editBtn);

    fireEvent.change(screen.getByLabelText(/Full Name/i), { target: { value: 'Updated User' } });
    fireEvent.change(screen.getByLabelText(/Phone Number/i), { target: { value: '7777777777' } });

    const saveBtn = screen.getByRole('button', { name: /Save/i });
    fireEvent.click(saveBtn);

    await waitFor(() => {
      expect(updateUserProfile).toHaveBeenCalled();
      const arg = (updateUserProfile as jest.Mock).mock.calls[0][0];
      expect(arg instanceof FormData).toBe(true);
      // Verify essential fields
      const fullName = arg.get('full_name');
      const mobile = arg.get('mobile_number');
      expect(fullName).toBe('Updated User');
      expect(mobile).toBe('7777777777');
    });
  });
});
