// Lightweight API client used across the app

type Json = any;

const API_BASE =
  (typeof process !== "undefined" && (process as any).env?.VITE_API_BASE_URL) ||
  "";

async function request<T = unknown>(
  path: string,
  init: RequestInit = {}
): Promise<{ data?: T; error?: Json }> {
  try {
    const isForm =
      typeof FormData !== "undefined" && init.body instanceof FormData;
    const res = await fetch(`${API_BASE}${path}`, {
      headers: {
        ...(isForm ? {} : { "Content-Type": "application/json" }),
        ...(init.headers || {}),
      },
      ...init,
    });

    const isJson = res.headers
      .get("content-type")
      ?.includes("application/json");
    const body = isJson ? await res.json() : await res.text();

    if (!res.ok) {
      // Attempt token refresh if JWT expired
      const code = (body as any)?.code;
      if (res.status === 401 && code === "token_not_valid") {
        const newAccess = await refreshAccessToken();
        if (newAccess) {
          const nextInit: RequestInit = { ...init };
          const nextHeaders: Record<string, string> = {
            ...(isForm ? {} : { "Content-Type": "application/json" }),
            ...((init.headers as any) || {}),
            Authorization: `Bearer ${newAccess}`,
          };
          nextInit.headers = nextHeaders;
          const retry = await fetch(`${API_BASE}${path}`, nextInit);
          const retryJson = retry.headers
            .get("content-type")
            ?.includes("application/json");
          const retryBody = retryJson ? await retry.json() : await retry.text();
          if (!retry.ok) return { error: retryBody as Json };
          return { data: retryBody as T };
        }
      }
      return { error: body as Json };
    }

    return { data: body as T };
  } catch (e) {
    return { error: "Network error" };
  }
}

function getAccessToken(): string | undefined {
  try {
    const raw = localStorage.getItem("authTokens");
    if (!raw) return undefined;
    const parsed = JSON.parse(raw);
    // Support either { access, refresh } or any token shape with 'access'
    return parsed?.access ?? parsed?.token ?? undefined;
  } catch {
    return undefined;
  }
}

function getRefreshToken(): string | undefined {
  try {
    const raw = localStorage.getItem("authTokens");
    if (!raw) return undefined;
    const parsed = JSON.parse(raw);
    return parsed?.refresh ?? undefined;
  } catch {
    return undefined;
  }
}

async function refreshAccessToken(): Promise<string | undefined> {
  const refresh = getRefreshToken();
  if (!refresh) return undefined;
  try {
    const res = await fetch(`${API_BASE}/api/accounts/token/refresh/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh }),
    });
    if (!res.ok) return undefined;
    const data = await res.json();
    const access = (data as any)?.access;
    if (!access) return undefined;
    // Persist new access token alongside existing refresh
    try {
      const raw = localStorage.getItem("authTokens");
      const tokens = raw ? JSON.parse(raw) : {};
      tokens.access = access;
      localStorage.setItem("authTokens", JSON.stringify(tokens));
    } catch {}
    return access as string;
  } catch {
    return undefined;
  }
}

export async function loginUser(payload: {
  mobile_number: string;
  password: string;
}) {
  // Backend returns { access, refresh } via SimpleJWT
  return request<{ access: string; refresh: string }>("/api/accounts/login/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function registerUser(payload: {
  full_name: string;
  mobile_number: string;
  password: string;
}) {
  // Backend RegisterView returns { tokens: {refresh, access}, user }
  return request<{
    tokens: { access: string; refresh: string };
    user: Record<string, unknown>;
  }>("/api/accounts/register/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function storeAuthData(tokens: unknown, user: unknown) {
  try {
    localStorage.setItem("authTokens", JSON.stringify(tokens));
    localStorage.setItem("authUser", JSON.stringify(user));
  } catch {
    // ignore storage errors
  }
}

export function logoutUser() {
  try {
    localStorage.removeItem("authTokens");
    localStorage.removeItem("authUser");
  } finally {
    // simple redirect back to login
    if (typeof window !== "undefined") {
      window.location.href = "/";
    }
  }
}

export async function fetchCurrentUser() {
  const token = getAccessToken();
  const headers: HeadersInit = token
    ? { Authorization: `Bearer ${token}` }
    : {};
  const res = await request<Record<string, unknown>>("/api/accounts/me/", {
    headers,
  });
  if (res.data) return res.data;
  throw new Error("Failed to fetch current user");
}

export async function updateUserProfile(
  payload: Record<string, unknown> | FormData
) {
  const token = getAccessToken();
  const headers: HeadersInit = {
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
  // Update the authenticated user's profile via accounts app
  return request<Record<string, unknown>>("/api/accounts/me/", {
    method: "PUT",
    headers,
    body: payload instanceof FormData ? payload : JSON.stringify(payload),
  });
}

export function getApiBase(): string {
  return (
    API_BASE || (typeof window !== "undefined" ? window.location.origin : "")
  );
}

export function resolveMediaUrl(path?: string | null): string {
  if (!path) return "";
  const s = String(path);
  if (s.startsWith("http") || s.startsWith("data:")) return s;
  const base = getApiBase();
  if (!base) return s;
  return `${base}${s.startsWith("/") ? s : `/${s}`}`;
}

export async function requestPasswordReset(payload: { email: string }) {
  // Attempt to call backend; if not implemented yet, return a friendly error
  const res = await request<{ detail?: string; message?: string }>(
    "/api/accounts/password/reset/",
    { method: "POST", body: JSON.stringify(payload) }
  );
  return res;
}
