import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";

import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Eye, EyeOff, User, Lock } from "lucide-react";
import { loginUser, storeAuthData, fetchCurrentUser } from "@/lib/api";

interface LoginProps {
  onSwitchToRegister?: () => void;
  onSwitchToForgotPassword?: () => void;
}

function Login({ onSwitchToRegister, onSwitchToForgotPassword }: LoginProps) {
  const navigate = useNavigate();
  const { setUser } = useAuth();
  const [mobileNumber, setMobileNumber] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleLogin = async () => {
    if (!mobileNumber || !password) {
      alert("Please enter both mobile number and password");
      return;
    }

    setIsLoading(true);

    try {
      const response = await loginUser({
        mobile_number: mobileNumber,
        password: password,
      });

      if (response.data) {
        // Store authentication tokens
        storeAuthData(response.data, null);

        // Try to fetch current user profile using the new token
        try {
          const me = await fetchCurrentUser();
          setUser({
            mobile_number: mobileNumber,
            ...(me as any),
          });
        } catch {
          // Fallback to minimal user when /me is unavailable
          setUser({ mobile_number: mobileNumber });
        }
        
        
        
        // Clear form
        setMobileNumber("");
        setPassword("");
        setRememberMe(false);
        
        // Navigate to Study page with a small delay to ensure state updates
        setTimeout(() => {
          navigate("/study", { replace: true });
        }, 100);
      } else if (response.error) {
        // Handle validation errors
        const error = response.error;
        if (error?.mobile_number && Array.isArray(error.mobile_number)) {
          alert(`Mobile number error: ${error.mobile_number[0]}`);
        } else if (error?.password && Array.isArray(error.password)) {
          alert(`Password error: ${error.password[0]}`);
        } else if (error?.detail && typeof error.detail === 'string') {
          alert(error.detail);
        } else if (error?.non_field_errors && Array.isArray(error.non_field_errors)) {
          alert(`Error: ${error.non_field_errors[0]}`);
        } else {
          alert("Login failed. Please check your credentials and try again.");
        }
        console.error("Login error:", error);
      }
    } catch (error) {
      alert("Network error. Please check your connection and try again.");
      console.error("Network error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSignUp = () => {
    if (onSwitchToRegister) {
      onSwitchToRegister(); // Used for dialog view
    } else {
      navigate('/register'); // Used for mobile page view
    }
  };

  const handleForgotPassword = () => {
    if (onSwitchToForgotPassword) {
      onSwitchToForgotPassword();
    } else {
      navigate('/forgot-password');
    }
  };


  return (
    <div className="p-0">
      <Card className="w-full rounded-none shadow-none border-none py-0">
        <CardHeader className="space-y-1 text-center pb-4 px-0">
          <CardTitle className="text-2xl font-bold">
            Welcome
          </CardTitle>
        </CardHeader>

        <div>
          <CardContent className="space-y-6 px-0">
            {/* Mobile Number Field */}
            <div className="space-y-2">
              <Label
                htmlFor="mobile"
                className="text-sm font-medium"
              >
                Mobile Number
              </Label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 h-4 w-4" />
                <Input
                  id="mobile"
                  type="tel"
                  placeholder="Enter your mobile number"
                  value={mobileNumber}
                  onChange={(e) => setMobileNumber(e.target.value)}
                  className="pl-10"
                  required
                />
              </div>
            </div>

            {/* Password Field */}
            <div className="space-y-2">
              <Label
                htmlFor="password"
                className="text-sm font-medium"
              >
                Password
              </Label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 h-4 w-4" />
                <Input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="pl-10 pr-10"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-slate-400 hover:text-slate-600 transition-colors"
                >
                  {showPassword ? (
                    <EyeOff className="h-4 w-4" />
                  ) : (
                    <Eye className="h-4 w-4" />
                  )}
                </button>
              </div>
            </div>

            {/* Remember Me and Forgot Password */}
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="remember"
                  checked={rememberMe}
                  onCheckedChange={(checked) => setRememberMe(checked === true)}
                />

                <Label
                  htmlFor="remember"
                  className="text-sm text-muted-foreground cursor-pointer select-none"
                >
                  Remember me
                </Label>
              </div>

              {/* Updated Forgot Password Link */}
              <button
                type="button"
                onClick={handleForgotPassword}
                className="text-sm text-blue-600 hover:text-blue-800 hover:underline transition-colors"
              >
                Forgot password?
              </button>
            </div>
          </CardContent>

          <CardFooter className="px-0">
            <Button
              onClick={handleLogin}
              size="lg"
              className="w-full text-white"
              disabled={isLoading}
            >
              {isLoading ? (
                <div className="flex items-center space-x-2">
                  <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
                  <span>Signing in...</span>
                </div>
              ) : (
                "Login"
              )}
            </Button>
          </CardFooter>
        </div>

        <div className="text-center py-2">
          <p className="text-sm text-muted-foreground">
            Don't have an account?{" "}
            <button
              type="button"
              onClick={handleSignUp}
              className="text-blue-600 hover:text-blue-800 hover:underline font-medium transition-colors"
            >
              Sign Up
            </button>
          </p>
        </div>

      </Card>
    </div>
  );
}

export default Login;
