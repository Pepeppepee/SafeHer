import React from "react";
import { View, Text, StyleSheet } from "react-native";
import { api } from "../api";
import { Option } from "../ui";
import { colors } from "../theme";

const SCENES = [
  { v: "mainstream", title: "🏛️ Mainstream landmark", sub: "The well-known spots — Durbar Squares, Boudhanath, Swayambhu" },
  { v: "hidden_gem", title: "💎 Hidden gem", sub: "Off the circuit — quiet temples, forests, viewpoints almost no one visits" },
  { v: "cafe_social", title: "☕ Café & social", sub: "Rooftop cafés, live music, a good strip to hang out on" },
];

export default function SceneScreen({ route, navigation }) {
  const { mood, crowd, distance } = route.params;

  async function findWith(scene) {
    navigation.navigate("Loading");
    const r = await api("/api/moods/find/", { mood, crowd_preference: crowd, distance, scene_preference: scene });
    if (r.ok && r.data.match) {
      navigation.replace("Match", { match: r.data.match, queryId: r.data.query.id, reviews: r.data.reviews, mood, crowd, distance, scene });
    } else {
      navigation.replace("Scene", { mood, crowd, distance });
      // A real app would toast this; kept simple for now.
      alert(r.data.message || "No matches found for that combo. Try a different kind of place.");
    }
  }

  return (
    <View style={styles.screen}>
      <Text style={styles.title}>What kind of place?</Text>
      <Text style={styles.sub}>So we don't just show you the same famous few every time.</Text>
      {SCENES.map((s) => (
        <Option key={s.v} title={s.title} subtitle={s.sub} onPress={() => findWith(s.v)} />
      ))}
      <Text style={styles.back} onPress={() => navigation.navigate("Mood")}>← Back</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.bg, padding: 20, paddingTop: 40 },
  title: { fontSize: 22, fontWeight: "700", color: colors.t, marginBottom: 8 },
  sub: { fontSize: 14, color: colors.ts, marginBottom: 20 },
  back: { fontSize: 13, color: colors.ts, textAlign: "center", marginTop: 12, textDecorationLine: "underline" },
});
