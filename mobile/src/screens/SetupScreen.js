import React, { useState } from "react";
import { View, Text, ScrollView, StyleSheet } from "react-native";
import { api } from "../api";
import { Btn, Option, Chip } from "../ui";
import { colors } from "../theme";

const TIERS = [
  { v: "first_timer", label: "Never been out alone" },
  { v: "cautious", label: "I have, but I'm careful" },
  { v: "confident", label: "I go solo all the time" },
];
const ANXIETIES = ["Empty streets", "Men staring", "No signal", "Hard to get back", "Being alone"];

export default function SetupScreen({ navigation }) {
  const [tier, setTier] = useState(null);
  const [anxieties, setAnxieties] = useState([]);

  function toggleAnxiety(a) {
    if (anxieties.includes(a)) setAnxieties(anxieties.filter((x) => x !== a));
    else if (anxieties.length < 3) setAnxieties([...anxieties, a]);
  }

  async function doSetup() {
    const r = await api("/api/accounts/profile/setup/", {
      comfort_tier: tier,
      anxiety_points: anxieties,
      interest_scores: { peace: 0.5, energy: 0.5, wonder: 0.5, reset: 0.5 },
    });
    if (r.ok) navigation.reset({ index: 0, routes: [{ name: "Mood" }] });
  }

  return (
    <ScrollView style={styles.screen} contentContainerStyle={{ padding: 20 }}>
      <Text style={styles.title}>Quick setup</Text>
      <Text style={styles.sub}>Two questions so we match you right.</Text>
      <Text style={styles.label}>How experienced are you solo?</Text>
      {TIERS.map((t) => (
        <Option key={t.v} title={t.label} selected={tier === t.v} onPress={() => setTier(t.v)} />
      ))}
      <Text style={[styles.label, { marginTop: 16 }]}>What makes you uneasy? (up to 3)</Text>
      <View style={{ flexDirection: "row", flexWrap: "wrap", marginBottom: 20 }}>
        {ANXIETIES.map((a) => (
          <Chip key={a} label={a} selected={anxieties.includes(a)} onPress={() => toggleAnxiety(a)} />
        ))}
      </View>
      <Btn title="Done — show me places" onPress={doSetup} disabled={!tier} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.bg },
  title: { fontSize: 22, fontWeight: "700", color: colors.t, marginBottom: 8 },
  sub: { fontSize: 14, color: colors.ts, marginBottom: 24 },
  label: { fontSize: 13, color: colors.ts, fontWeight: "600", marginBottom: 8 },
});
