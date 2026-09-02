import React, { useState } from "react";
import { View, Text, StyleSheet } from "react-native";
import { api } from "../api";
import { Btn, Blob } from "../ui";
import { colors } from "../theme";

function todayISO() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

export default function BuddyScreen({ route, navigation }) {
  const { experienceId, experienceName } = route.params;
  const [result, setResult] = useState(null); // { icon, title, sub, threadId }

  async function want(wantsBuddy) {
    const r = await api("/api/buddies/intent/", { experience_id: experienceId, intended_date: todayISO(), wants_buddy: wantsBuddy });
    if (!r.ok) {
      setResult({ icon: "😕", title: "Couldn't set that up", sub: r.data.error || "Try again from your next match." });
      return;
    }
    if (!wantsBuddy) {
      setResult({ icon: "🧘", title: "Solo it is", sub: "You've got this. We'll still be right here if you need anything." });
      return;
    }
    if (r.data.matched && r.data.thread) {
      setResult({ icon: "🎉", title: "You're matched!", sub: `Another woman is heading to ${experienceName} too. Say hi — the chat closes 48 hours after your trip.`, threadId: r.data.thread.id });
    } else {
      setResult({ icon: "⏳", title: "You're on the list", sub: "No one else has opted in for this spot yet — we'll match you the moment someone does. Check My Buddies later." });
    }
  }

  if (result) {
    return (
      <View style={styles.screen}>
        <Blob emoji={result.icon} />
        <Text style={styles.title}>{result.title}</Text>
        <Text style={styles.sub}>{result.sub}</Text>
        {result.threadId ? (
          <Btn title="Say hi 👋" onPress={() => navigation.replace("Chat", { threadId: result.threadId })} />
        ) : null}
        <Btn title="Continue" outline style={{ marginTop: 12 }} onPress={() => navigation.reset({ index: 0, routes: [{ name: "Go" }] })} />
      </View>
    );
  }

  return (
    <View style={styles.screen}>
      <Blob emoji="👯" />
      <Text style={styles.title}>Want company for this one?</Text>
      <Text style={styles.sub}>We'll blind-match you with another woman heading to the same place, same day. No profiles, no photos — just a private chat until the trip's done.</Text>
      <Btn title="Yes, find me a buddy" onPress={() => want(true)} />
      <Btn title="No, I'm good solo" outline style={{ marginTop: 12 }} onPress={() => want(false)} />
    </View>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.bg, padding: 24, paddingTop: 80, alignItems: "center" },
  title: { fontSize: 20, fontWeight: "700", color: colors.t, marginBottom: 8, textAlign: "center" },
  sub: { fontSize: 14, color: colors.ts, textAlign: "center", marginBottom: 24, lineHeight: 20 },
});
