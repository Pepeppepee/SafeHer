import React from "react";
import { View, Text, StyleSheet } from "react-native";
import { Option } from "../ui";
import { colors } from "../theme";

const REASONS = [
  { v: "wrong_mood", label: "Wrong mood" },
  { v: "too_far", label: "Too far" },
  { v: "not_safe", label: "Doesn't feel safe" },
  { v: "been_there", label: "Already been" },
  { v: "bad_timing", label: "Bad timing" },
];

export default function DeclineScreen({ route, navigation }) {
  function pick(reason) {
    navigation.goBack();
    // onPick (the match screen's respond fn) navigates onward itself once done.
    route.params.onPick("declined", reason);
  }

  return (
    <View style={styles.screen}>
      <Text style={styles.title}>What didn't fit?</Text>
      <Text style={styles.sub}>Helps us get it right.</Text>
      {REASONS.map((r) => (
        <Option key={r.v} title={r.label} onPress={() => pick(r.v)} />
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.bg, padding: 20, paddingTop: 40 },
  title: { fontSize: 20, fontWeight: "700", color: colors.t, marginBottom: 8 },
  sub: { fontSize: 14, color: colors.ts, marginBottom: 20 },
});
