import AsyncStorage from "@react-native-async-storage/async-storage";

// Points at the same Django backend the web app uses — one backend serves both.
// Set EXPO_PUBLIC_API_BASE (in mobile/.env or the build environment) to switch
// between the deployed server and a local tunnel without editing code. Expo inlines
// EXPO_PUBLIC_* variables at build time, so this is a constant in the shipped bundle.
export const API_BASE =
  process.env.EXPO_PUBLIC_API_BASE || "https://silvicolous-elianna-unintendedly.ngrok-free.dev";

const TOKEN_KEY = "safeher_token";
// AsyncStorage (not SecureStore) so this works identically on iOS, Android, and web —
// an auth token here doesn't warrant Keychain-level protection for this app.

export async function saveToken(token) {
  await AsyncStorage.setItem(TOKEN_KEY, token);
}
export async function getToken() {
  return AsyncStorage.getItem(TOKEN_KEY);
}
export async function clearToken() {
  await AsyncStorage.removeItem(TOKEN_KEY);
}

export async function api(path, body) {
  const token = await getToken();
  const headers = {
    "Content-Type": "application/json",
    // Skips ngrok's browser-warning interstitial page, which would otherwise
    // return HTML instead of JSON to a non-browser client like this app.
    "ngrok-skip-browser-warning": "true",
  };
  if (token) headers["Authorization"] = `Token ${token}`;

  const res = await fetch(`${API_BASE}${path}`, {
    method: body ? "POST" : "GET",
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  let data = {};
  try {
    data = await res.json();
  } catch {
    // non-JSON response (e.g. a raw error page) — treat as failure below
  }
  return { ok: res.ok, status: res.status, data };
}
