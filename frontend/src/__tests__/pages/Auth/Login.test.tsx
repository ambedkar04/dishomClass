// React import not needed with new JSX transform
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter as Router } from 'react-router-dom';
import { AuthProvider } from '@/contexts/AuthContext';
import Login from '../../../pages/Auth/Login';
import '@testing-library/jest-dom';

// Mock the loginUser and storeAuthData functions
jest.mock('../../../lib/api', () => ({
  loginUser: jest.fn(),
  storeAuthData: jest.fn(),
}));

describe('Login Component', () => {
  const mockLoginUser = require('../../../lib/api').loginUser;
  const mockStoreAuthData = require('../../../lib/api').storeAuthData;

  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();
  });

  const renderLogin = () => {
    render(
      <AuthProvider>
        <Router>
          <Login />
        </Router>
      </AuthProvider>
    );
  };

  test('renders login form with email and password fields', () => {
    renderLogin();
    
    // Check if the login form is rendered with all necessary elements
    expect(screen.getByLabelText(/Mobile Number/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
    expect(screen.getByText(/Don't have an account?/i)).toBeInTheDocument();
    expect(screen.getByText(/Forgot Password?/i)).toBeInTheDocument();
  });

  test('shows error when submitting empty form', async () => {
    renderLogin();
    
    // Click the login button without entering any data
    const loginButton = screen.getByRole('button', { name: /login/i });
    fireEvent.click(loginButton);
    
    // Check if error message is shown
    await waitFor(() => {
      expect(screen.getByText(/Please enter both mobile number and password/i)).toBeInTheDocument();
    });
    
    // Ensure the API was not called
    expect(mockLoginUser).not.toHaveBeenCalled();
  });

  test('handles successful login', async () => {
    // Mock a successful API response
    const mockResponse = {
      data: {
        access: 'mock-access-token',
        refresh: 'mock-refresh-token'
      }
    };
    mockLoginUser.mockResolvedValueOnce(mockResponse);
    
    renderLogin();
    
    // Fill in the form
    fireEvent.change(screen.getByLabelText(/Mobile Number/i), { 
      target: { value: '1234567890' } 
    });
    fireEvent.change(screen.getByLabelText(/Password/i), { 
      target: { value: 'password123' } 
    });
    
    // Submit the form
    const loginButton = screen.getByRole('button', { name: /login/i });
    fireEvent.click(loginButton);
    
    // Check if the API was called with the correct data
    await waitFor(() => {
      expect(mockLoginUser).toHaveBeenCalledWith({
        mobile_number: '1234567890',
        password: 'password123'
      });
      
      // Check if storeAuthData was called with the correct tokens
      expect(mockStoreAuthData).toHaveBeenCalledWith(
        mockResponse.data,
        null
      );
      
      // Check if the success message is shown
      expect(screen.getByText(/Login successful! Welcome back./i)).toBeInTheDocument();
    });
  });

  test('handles login error with invalid credentials', async () => {
    // Mock an error response
    const errorResponse = {
      error: {
        detail: 'No active account found with the given credentials'
      }
    };
    mockLoginUser.mockResolvedValueOnce(errorResponse);
    
    renderLogin();
    
    // Fill in the form with invalid credentials
    fireEvent.change(screen.getByLabelText(/Mobile Number/i), { 
      target: { value: 'wronguser' } 
    });
    fireEvent.change(screen.getByLabelText(/Password/i), { 
      target: { value: 'wrongpassword' } 
    });
    
    // Submit the form
    const loginButton = screen.getByRole('button', { name: /login/i });
    fireEvent.click(loginButton);
    
    // Check if the error message is shown
    await waitFor(() => {
      expect(screen.getByText(/No active account found with the given credentials/i)).toBeInTheDocument();
    });
  });

  test('navigates to register page when sign up link is clicked', () => {
    renderLogin();
    
    // Click the sign up link
    const signUpLink = screen.getByText(/Sign up/i);
    fireEvent.click(signUpLink);
    
    // Check if the URL changed to /register
    expect(window.location.pathname).toBe('/register');
  });

  test('navigates to forgot password page when forgot password link is clicked', () => {
    renderLogin();
    
    // Click the forgot password link
    const forgotPasswordLink = screen.getByText(/Forgot Password?/i);
    fireEvent.click(forgotPasswordLink);
    
    // Check if the URL changed to /forgot-password
    expect(window.location.pathname).toBe('/forgot-password');
  });
});
