import React, { useState } from "react";
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import { api } from "../api";
import { Btn, Tag } from "../ui";
import { colors, SCENE_META, SAFE_META, SAFE_ORDER } from "../theme";

function SafetyRow({ item, defaultOpen }) {
  const [open, setOpen] = useState(defaultOpen);
  const meta = SAFE_META[item.category] || { icon: "ℹ️", label: item.category };
  return (
    <TouchableOpacity style={styles.saccRow} onPress={() => setOpen(!open)} activeOpacity={0.8}>
      <View style={styles.saccHead}>
        <View style={styles.saccIcon}><Text>{meta.icon}</Text></View>
        <Text style={styles.saccLabel}>{meta.label}</Text>
        <Text style={styles.chev}>{open ? "︿" : "﹀"}</Text>
      </View>
      {open ? (
        <Text style={styles.saccBody}>
          {item.content}
          {item.transport_back ? `\n🚗 ${item.transport_back}` : ""}
        </Text>
      ) : null}
    </TouchableOpacity>
  );
}

export default function MatchScreen({ route, navigation }) {
  const { match, queryId, reviews, mood, crowd, distance, scene } = route.params;
  const intel = [...(match.safety_intel || [])].sort(
    (a, b) => SAFE_ORDER.indexOf(a.category) - SAFE_ORDER.indexOf(b.category)
  );
  const sceneMeta = SCENE_META[match.scene_type];

  async function respond(decision, reason) {
    const r = await api("/api/moods/respond/", { experience_id: match.id, mood_query_id: queryId, decision, decline_reason: reason || "" });
    if (!r.ok) return;
    if (decision === "going") {
      navigation.navigate("Buddy", { experienceId: match.id, experienceName: match.name });
    } else {
      // Declining re-searches immediately with the same preferences instead of
      // sending her back to pick mood/crowd/distance/scene from scratch.
      navigation.navigate("Loading");
      const r2 = await api("/api/moods/find/", { mood, crowd_preference: crowd, distance, scene_preference: scene });
      if (r2.ok && r2.data.match) {
        navigation.replace("Match", { match: r2.data.match, queryId: r2.data.query.id, reviews: r2.data.reviews, mood, crowd, distance, scene });
      } else {
        navigation.replace("Scene", { mood, crowd, distance });
        alert(r2.data.message || "No more matches for that combo today.");
      }
    }
  }

  return (
    <ScrollView style={styles.screen}>
      <Text style={styles.eyebrow}>YOUR MATCH</Text>
      <View style={styles.card}>
        <LinearGradient colors={[colors.lav, colors.a, colors.peach]} start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }} style={styles.header}>
          <Text style={styles.name}>{match.name}</Text>
          <Text style={styles.area}>{match.area}</Text>
          {sceneMeta ? <Text style={styles.sceneBadge}>{sceneMeta.emoji} {sceneMeta.label}</Text> : null}
        </LinearGradient>
        <View style={styles.body}>
          <View style={styles.tagRow}>
            {(match.vibe_tags || []).map((t) => <Tag key={t} label={t} />)}
          </View>
          {match.match_reasons?.map((r, i) => (
            <View key={i} style={styles.infoRow}><Text style={styles.infoText}>✓ {r}</Text></View>
          ))}
          <Text style={styles.sectionLbl}>🛡️ Safety info — tap to open</Text>
          {match.total_visitors > 0 ? (
            <View style={styles.statPill}><Text style={styles.statText}>💛 {match.safety_percentage}% felt safe · 👭 {match.total_visitors} women visited</Text></View>
          ) : (
            <View style={styles.statPill}><Text style={styles.statText}>🌱 Be the first to check in here</Text></View>
          )}
          {intel.map((item, i) => <SafetyRow key={i} item={item} defaultOpen={i === 0} />)}
          {reviews?.map((rv, i) => (
            <View key={i} style={styles.review}>
              <Text style={styles.reviewText}>💬 "{rv}"</Text>
              <Text style={styles.reviewAt}>— a woman who visited recently</Text>
            </View>
          ))}
          <View style={styles.btnRow}>
            <View style={{ flex: 1, marginRight: 8 }}><Btn title="I'm going" onPress={() => respond("going")} /></View>
            <View style={{ flex: 1 }}><Btn title="Not this time" outline onPress={() => navigation.navigate("Decline", { onPick: respond })} /></View>
          </View>
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.bg, padding: 16 },
  eyebrow: { fontSize: 11, color: colors.tm, letterSpacing: 0.5, marginBottom: 12 },
  card: { backgroundColor: colors.c, borderRadius: 22, overflow: "hidden", marginBottom: 30 },
  header: { height: 130, justifyContent: "flex-end", padding: 18 },
  name: { fontSize: 19, fontWeight: "700", color: "#fff" },
  area: { fontSize: 13, color: "rgba(255,255,255,.95)" },
  sceneBadge: { fontSize: 11.5, fontWeight: "700", color: "#fff", marginTop: 2 },
  body: { padding: 18 },
  tagRow: { flexDirection: "row", flexWrap: "wrap", marginBottom: 12 },
  infoRow: { backgroundColor: colors.lavL, borderRadius: 12, padding: 10, marginBottom: 8 },
  infoText: { color: colors.lavD || "#5B4F94", fontSize: 13 },
  sectionLbl: { fontSize: 13, fontWeight: "700", color: colors.ts, marginVertical: 8 },
  statPill: { alignSelf: "flex-start", backgroundColor: colors.sageL, borderRadius: 999, paddingVertical: 8, paddingHorizontal: 14, marginBottom: 12 },
  statText: { color: colors.sageD, fontWeight: "700", fontSize: 13 },
  saccRow: { backgroundColor: colors.sageL, borderRadius: 14, padding: 12, marginBottom: 8 },
  saccHead: { flexDirection: "row", alignItems: "center" },
  saccIcon: { width: 26, height: 26, borderRadius: 13, backgroundColor: "#fff", alignItems: "center", justifyContent: "center", marginRight: 10 },
  saccLabel: { flex: 1, fontWeight: "700", color: colors.sageD, fontSize: 13.5 },
  chev: { color: colors.sageD, opacity: 0.6 },
  saccBody: { marginTop: 10, marginLeft: 36, color: colors.sageD, fontSize: 13, lineHeight: 19 },
  review: { backgroundColor: colors.peachL, borderRadius: 14, padding: 12, marginBottom: 10 },
  reviewText: { color: colors.peachD, fontStyle: "italic", fontSize: 13 },
  reviewAt: { color: colors.peachD, opacity: 0.75, fontSize: 11, fontWeight: "600", marginTop: 4 },
  btnRow: { flexDirection: "row", marginTop: 8 },
});
