import React, { useState } from "react";
import { View, Text, TextInput, StyleSheet, KeyboardAvoidingView, Platform } from "react-native";
import { api } from "../api";
import { useAuth } from "../context/AuthContext";
import { Btn, Blob } from "../ui";
import { colors } from "../theme";

export default function LoginScreen({ navigation }) {
  const [phone, setPhone] = useState("");
  const [error, setError] = useState("");
  const { signIn } = useAuth();

  async function doLogin() {
    if (!phone.trim()) return;
    setError("");
    const r = await api("/api/accounts/login/", { phone: phone.trim() });
    if (r.ok) {
      await signIn(r.data, r.data.token);
      navigation.reset({ index: 0, routes: [{ name: r.data.has_profile ? "Mood" : "Setup" }] });
    } else {
      setError(r.data.error || "Login failed");
    }
  }

  return (
    <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : undefined} style={styles.screen}>
      <View style={styles.top}>
        <Blob emoji="🌸" />
        <Text style={styles.brand}>SafeHer</Text>
        <Text style={styles.sub}>Tell me your mood, I'll find your place — safely, as a woman, in the valley.</Text>
      </View>
      <TextInput
        style={styles.input}
        placeholder="Your phone number"
        placeholderTextColor={colors.tm}
        keyboardType="phone-pad"
        value={phone}
        onChangeText={setPhone}
      />
      <Btn title="Enter" onPress={doLogin} />
      <Text style={styles.link} onPress={() => navigation.navigate("Join")}>
        New here? <Text style={styles.linkBold}>Join with an invite code</Text>
      </Text>
      {error ? <Text style={styles.error}>{error}</Text> : null}
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.bg, padding: 20, justifyContent: "center" },
  top: { alignItems: "center", marginBottom: 28 },
  brand: { fontSize: 26, fontWeight: "700", color: colors.ad, marginBottom: 8 },
  sub: { fontSize: 14, color: colors.ts, textAlign: "center", lineHeight: 20 },
  input: { backgroundColor: colors.c, borderWidth: 1.5, borderColor: colors.b, borderRadius: 14, padding: 14, fontSize: 15, marginBottom: 12, color: colors.t },
  link: { fontSize: 13, color: colors.ts, textAlign: "center", marginTop: 16 },
  linkBold: { color: colors.ad, fontWeight: "700", textDecorationLine: "underline" },
  error: { backgroundColor: "#FEE8E7", color: "#9B2C2C", padding: 12, borderRadius: 12, fontSize: 13, marginTop: 16 },
});
