import React, { useCallback, useState } from "react";
import { View, Text, StyleSheet, FlatList, TouchableOpacity, Alert } from "react-native";
import { useFocusEffect } from "@react-navigation/native";
import * as Clipboard from "expo-clipboard";
import { api } from "../api";
import { Btn, Blob } from "../ui";
import { colors } from "../theme";

export default function InvitesScreen({ navigation }) {
  const [data, setData] = useState({ codes: [], remaining: null, max: null });

  const load = useCallback(() => {
    api("/api/accounts/invites/").then((r) => { if (r.ok) setData(r.data); });
  }, []);

  useFocusEffect(load);

  async function generate() {
    const r = await api("/api/accounts/invites/generate/", {});
    if (r.ok) load();
    else Alert.alert("Couldn't generate a code", r.data.error || "");
  }

  function copy(code) {
    Clipboard.setStringAsync(code);
    Alert.alert("Copied", `${code} copied — send it to a friend.`);
  }

  const unlimited = data.max === null;
  const capped = !unlimited && data.remaining <= 0;

  return (
    <View style={styles.screen}>
      <View style={styles.header}>
        <Text style={styles.title}>Invite friends 💌</Text>
        <TouchableOpacity onPress={() => navigation.goBack()}><Text style={{ fontSize: 18 }}>✕</Text></TouchableOpacity>
      </View>
      <Text style={styles.sub}>
        This app is invite-only, by design — it keeps the community small and trusted.{" "}
        {unlimited ? "You have unlimited invites." : `You have ${data.remaining} of ${data.max} invites left.`}
      </Text>
      <Btn title="Generate a new code" onPress={generate} disabled={capped} />
      <FlatList
        style={{ marginTop: 20 }}
        data={data.codes}
        keyExtractor={(c) => c.code}
        ListEmptyComponent={<Blob emoji="💌" />}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <Text style={styles.code}>{item.code}</Text>
            {item.used_by_name ? (
              <Text style={styles.used}>✓ used by {item.used_by_name}</Text>
            ) : (
              <TouchableOpacity onPress={() => copy(item.code)}><Text style={styles.copy}>tap to copy</Text></TouchableOpacity>
            )}
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.bg, padding: 20, paddingTop: 50 },
  header: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", marginBottom: 10 },
  title: { fontSize: 20, fontWeight: "700", color: colors.t },
  sub: { fontSize: 13.5, color: colors.ts, lineHeight: 19, marginBottom: 16 },
  card: { backgroundColor: colors.c, borderRadius: 16, padding: 14, marginBottom: 10, elevation: 2 },
  code: { fontWeight: "700", fontSize: 15, letterSpacing: 1, color: colors.t },
  used: { fontSize: 12, color: colors.sageD, marginTop: 4 },
  copy: { fontSize: 12, color: colors.ts, textDecorationLine: "underline", marginTop: 4 },
});
