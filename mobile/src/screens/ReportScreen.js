import React, { useState } from "react";
import { View, Text, StyleSheet } from "react-native";
import { api } from "../api";
import { Option } from "../ui";
import { colors } from "../theme";

const REASONS = [
  { v: "harassment", label: "Harassment" },
  { v: "inappropriate", label: "Inappropriate behavior" },
  { v: "not_woman", label: "Might not be a woman" },
  { v: "spam", label: "Spam" },
  { v: "other", label: "Other" },
];

export default function ReportScreen({ route, navigation }) {
  const { threadId, members } = route.params;
  const [target, setTarget] = useState(null);
  const others = members.filter((m) => !m.is_me);

  async function submit(reason) {
    const r = await api(`/api/buddies/threads/${threadId}/report/`, { reported_user_id: target.id, reason });
    alert(r.ok ? r.data.message : r.data.error || "Could not submit report");
    navigation.goBack();
  }

  if (!target) {
    return (
      <View style={styles.screen}>
        <Text style={styles.title}>Who's this about?</Text>
        <Text style={styles.sub}>Your report is private. It takes two reports to act.</Text>
        {others.length === 0 ? (
          <Text style={styles.sub}>No one else in this chat yet.</Text>
        ) : (
          others.map((m) => <Option key={m.id} title={m.first_name} onPress={() => setTarget(m)} />)
        )}
        <Text style={styles.back} onPress={() => navigation.goBack()}>Cancel</Text>
      </View>
    );
  }

  return (
    <View style={styles.screen}>
      <Text style={styles.title}>What happened?</Text>
      <Text style={styles.sub}>Helps us keep this space safe.</Text>
      {REASONS.map((r) => <Option key={r.v} title={r.label} onPress={() => submit(r.v)} />)}
    </View>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.bg, padding: 20, paddingTop: 60 },
  title: { fontSize: 20, fontWeight: "700", color: colors.t, marginBottom: 8 },
  sub: { fontSize: 14, color: colors.ts, marginBottom: 20 },
  back: { textAlign: "center", color: colors.ts, marginTop: 16, textDecorationLine: "underline" },
});
