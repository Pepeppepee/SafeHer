import React, { createContext, useContext, useState } from "react";
import { saveToken, clearToken } from "../api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null); // { id, first_name }
  const [profile, setProfile] = useState(null); // TravelerProfile data

  async function signIn(userData, token) {
    await saveToken(token);
    setUser(userData);
  }
  async function signOut() {
    await clearToken();
    setUser(null);
    setProfile(null);
  }

  return (
    <AuthContext.Provider value={{ user, setUser, profile, setProfile, signIn, signOut }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
