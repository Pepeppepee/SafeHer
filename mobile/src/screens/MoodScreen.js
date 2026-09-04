import React, { useEffect, useState, useCallback } from "react";
import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from "react-native";
import { useFocusEffect } from "@react-navigation/native";
import { api } from "../api";
import { useAuth } from "../context/AuthContext";
import { Chip } from "../ui";
import { colors } from "../theme";

const MOODS = [
  { v: "peace", emoji: "🌅", label: "Peace", desc: "stillness, sunsets, breathe", bg: colors.lavL },
  { v: "energy", emoji: "⚡", label: "Energy", desc: "concerts, crowds, buzz", bg: colors.peachL },
  { v: "wonder", emoji: "✨", label: "Wonder", desc: "new streets, hidden gems", bg: colors.sageL },
  { v: "reset", emoji: "🍃", label: "Reset", desc: "river, silence, nothing", bg: "#E5F2F6" },
];

export default function MoodScreen({ navigation }) {
  const { user, profile, setProfile } = useAuth();
  const [mood, setMood] = useState(null);
  const [crowd, setCrowd] = useState(null);
  const [distance, setDistance] = useState(null);
  const [hasThreads, setHasThreads] = useState(false);

  const loadProfile = useCallback(async () => {
    const r = await api("/api/accounts/profile/");
    if (r.ok) setProfile(r.data);
    const t = await api("/api/buddies/threads/");
    if (t.ok) setHasThreads(t.data.length > 0);
  }, []);

  useFocusEffect(
    useCallback(() => {
      setMood(null); setCrowd(null); setDistance(null);
      loadProfile();
    }, [loadProfile])
  );

  function goNext() {
    navigation.navigate("Scene", { mood, crowd, distance });
  }

  return (
    <ScrollView style={styles.screen} contentContainerStyle={{ padding: 20 }}>
      <View style={styles.navrow}>
        <View style={{ flex: 1 }}>
          <Text style={styles.title}>Hey {user?.first_name}, how do you want to feel today?</Text>
        </View>
        <View style={{ flexDirection: "row", gap: 8 }}>
          <TouchableOpacity style={styles.navIcon} onPress={() => navigation.navigate("Invites")}>
            <Text style={{ fontSize: 18 }}>💌</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.navIcon} onPress={() => navigation.navigate("Threads")}>
            <Text style={{ fontSize: 18 }}>👭</Text>
            {hasThreads && <View style={styles.dot} />}
          </TouchableOpacity>
        </View>
      </View>
      {profile ? (
        <View style={styles.badge}>
          <Text style={styles.badgeText}>🏅 {profile.personality_label || "Explorer"} · {profile.trips_completed} trip{profile.trips_completed === 1 ? "" : "s"}</Text>
        </View>
      ) : null}
      <View style={styles.grid}>
        {MOODS.map((m) => (
          <TouchableOpacity key={m.v} style={[styles.moodCard, { backgroundColor: m.bg }, mood === m.v && styles.moodCardSelected]} onPress={() => setMood(m.v)}>
            <Text style={{ fontSize: 26 }}>{m.emoji}</Text>
            <Text style={styles.moodLabel}>{m.label}</Text>
            <Text style={styles.moodDesc}>{m.desc}</Text>
          </TouchableOpacity>
        ))}
      </View>
      <Text style={styles.label}>I'd rather be</Text>
      <View style={styles.row}>
        <Chip label="Somewhere quiet" selected={crowd === "quiet"} onPress={() => setCrowd("quiet")} />
        <Chip label="Around people" selected={crowd === "social"} onPress={() => setCrowd("social")} />
      </View>
      <Text style={styles.label}>How far?</Text>
      <View style={styles.row}>
        <Chip label="Walkable" selected={distance === "walkable"} onPress={() => setDistance("walkable")} />
        <Chip label="Under 1hr" selected={distance === "under_1hr"} onPress={() => setDistance("under_1hr")} />
        <Chip label="Day trip" selected={distance === "day_trip"} onPress={() => setDistance("day_trip")} />
      </View>
      <TouchableOpacity
        style={[styles.findBtn, !(mood && crowd && distance) && { opacity: 0.4 }]}
        disabled={!(mood && crowd && distance)}
        onPress={goNext}
      >
        <Text style={styles.findBtnText}>Find my place</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.bg },
  navrow: { flexDirection: "row", alignItems: "flex-start", marginBottom: 8 },
  title: { fontSize: 20, fontWeight: "700", color: colors.t },
  navIcon: { width: 42, height: 42, borderRadius: 21, backgroundColor: colors.c, alignItems: "center", justifyContent: "center", elevation: 2 },
  dot: { position: "absolute", top: 2, right: 2, width: 9, height: 9, borderRadius: 5, backgroundColor: colors.a, borderWidth: 2, borderColor: colors.bg },
  badge: { alignSelf: "flex-start", backgroundColor: colors.al, paddingVertical: 7, paddingHorizontal: 14, borderRadius: 999, marginBottom: 16, marginTop: 8 },
  badgeText: { color: colors.ad, fontWeight: "700", fontSize: 12.5 },
  grid: { flexDirection: "row", flexWrap: "wrap", justifyContent: "space-between", marginBottom: 10 },
  moodCard: { width: "48%", borderRadius: 18, padding: 16, marginBottom: 10 },
  moodCardSelected: { borderWidth: 2, borderColor: colors.a },
  moodLabel: { fontFamily: undefined, fontSize: 15, fontWeight: "700", marginTop: 8, color: colors.t },
  moodDesc: { fontSize: 11.5, color: colors.ts, marginTop: 2 },
  label: { fontSize: 13, color: colors.ts, fontWeight: "600", marginBottom: 8, marginTop: 8 },
  row: { flexDirection: "row", flexWrap: "wrap", marginBottom: 8 },
  findBtn: { backgroundColor: colors.a, borderRadius: 999, paddingVertical: 15, alignItems: "center", marginTop: 16 },
  findBtnText: { color: "#fff", fontWeight: "700", fontSize: 15 },
});
