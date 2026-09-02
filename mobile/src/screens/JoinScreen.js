import React, { useState } from "react";
import { View, Text, TextInput, StyleSheet, KeyboardAvoidingView, Platform } from "react-native";
import { api } from "../api";
import { useAuth } from "../context/AuthContext";
import { Btn, Blob } from "../ui";
import { colors } from "../theme";

export default function JoinScreen({ navigation }) {
  const [code, setCode] = useState("");
  const [phone, setPhone] = useState("");
  const [name, setName] = useState("");
  const [error, setError] = useState("");
  const { signIn } = useAuth();

  async function doJoin() {
    if (!code.trim() || !phone.trim() || !name.trim()) {
      setError("Fill in all three to continue.");
      return;
    }
    setError("");
    const r = await api("/api/accounts/signup/", { invite_code: code.trim(), phone: phone.trim(), first_name: name.trim() });
    if (r.ok) {
      await signIn(r.data, r.data.token);
      navigation.reset({ index: 0, routes: [{ name: "Setup" }] });
    } else {
      setError(r.data.error || "Could not create account");
    }
  }

  return (
    <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : undefined} style={styles.screen}>
      <View style={styles.top}>
        <Blob emoji="💌" />
        <Text style={styles.title}>You've been invited</Text>
        <Text style={styles.sub}>This app is invite-only, by design — it keeps the community small and trusted.</Text>
      </View>
      <TextInput style={styles.input} placeholder="Invite code" placeholderTextColor={colors.tm} autoCapitalize="characters" value={code} onChangeText={setCode} />
      <TextInput style={styles.input} placeholder="Your phone number" placeholderTextColor={colors.tm} keyboardType="phone-pad" value={phone} onChangeText={setPhone} />
      <TextInput style={styles.input} placeholder="Your first name" placeholderTextColor={colors.tm} value={name} onChangeText={setName} />
      <Btn title="Create my account" onPress={doJoin} />
      <Text style={styles.link} onPress={() => navigation.goBack()}>← Back to login</Text>
      {error ? <Text style={styles.error}>{error}</Text> : null}
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.bg, padding: 20, justifyContent: "center" },
  top: { alignItems: "center", marginBottom: 28 },
  title: { fontSize: 22, fontWeight: "700", color: colors.t, marginBottom: 8 },
  sub: { fontSize: 14, color: colors.ts, textAlign: "center", lineHeight: 20 },
  input: { backgroundColor: colors.c, borderWidth: 1.5, borderColor: colors.b, borderRadius: 14, padding: 14, fontSize: 15, marginBottom: 12, color: colors.t },
  link: { fontSize: 13, color: colors.ts, textAlign: "center", marginTop: 16, textDecorationLine: "underline" },
  error: { backgroundColor: "#FEE8E7", color: "#9B2C2C", padding: 12, borderRadius: 12, fontSize: 13, marginTop: 16 },
});
