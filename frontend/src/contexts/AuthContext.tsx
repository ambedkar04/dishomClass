import React, { createContext, useContext, useEffect, useMemo, useState } from "react";

export type User = {
  id?: string | number;
  full_name?: string;
  mobile_number?: string;
  email?: string;
  profile?: {
    state?: string;
    district?: string;
    pincode?: string;
    current_class?: string;
    village?: string;
    profile_image?: string;
  };
  [key: string]: unknown;
};

type AuthContextValue = {
  user: User | null;
  setUser: React.Dispatch<React.SetStateAction<User | null>>;
  hydrated: boolean;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    try {
      const cached = localStorage.getItem("authUser");
      if (cached) {
        setUser(JSON.parse(cached));
      }
    } catch {}
    finally {
      setHydrated(true);
    }
  }, []);

  useEffect(() => {
    try {
      if (user) localStorage.setItem("authUser", JSON.stringify(user));
      else localStorage.removeItem("authUser");
    } catch {}
  }, [user]);

  const value = useMemo(() => ({ user, setUser, hydrated }), [user, hydrated]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
