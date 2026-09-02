import React from "react";
import { Text, TouchableOpacity, View, StyleSheet } from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import { colors } from "./theme";

export function Btn({ title, onPress, outline, disabled, style }) {
  if (outline) {
    return (
      <TouchableOpacity onPress={onPress} disabled={disabled} style={[styles.btnOutline, disabled && styles.disabled, style]}>
        <Text style={styles.btnOutlineText}>{title}</Text>
      </TouchableOpacity>
    );
  }
  return (
    <TouchableOpacity onPress={onPress} disabled={disabled} activeOpacity={0.85} style={[disabled && styles.disabled, style]}>
      <LinearGradient colors={[colors.a, "#F0567A"]} start={{ x: 0, y: 0 }} end={{ x: 1, y: 0 }} style={styles.btn}>
        <Text style={styles.btnText}>{title}</Text>
      </LinearGradient>
    </TouchableOpacity>
  );
}

export function Blob({ emoji, size = 84 }) {
  return (
    <View style={[styles.blob, { width: size, height: size, borderRadius: size * 0.4 }]}>
      <Text style={{ fontSize: size * 0.4 }}>{emoji}</Text>
    </View>
  );
}

export function Chip({ label, selected, onPress }) {
  return (
    <TouchableOpacity onPress={onPress} style={[styles.chip, selected && styles.chipSelected]}>
      <Text style={[styles.chipText, selected && styles.chipTextSelected]}>{label}</Text>
    </TouchableOpacity>
  );
}

export function Option({ title, subtitle, selected, onPress }) {
  return (
    <TouchableOpacity onPress={onPress} style={[styles.option, selected && styles.optionSelected]}>
      <Text style={styles.optionTitle}>{title}</Text>
      {subtitle ? <Text style={styles.optionSubtitle}>{subtitle}</Text> : null}
    </TouchableOpacity>
  );
}

export function Tag({ label }) {
  return (
    <View style={styles.tag}>
      <Text style={styles.tagText}>{label}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  btn: { paddingVertical: 15, borderRadius: 999, alignItems: "center" },
  btnText: { color: "#fff", fontSize: 15, fontWeight: "700" },
  btnOutline: { paddingVertical: 15, borderRadius: 999, alignItems: "center", borderWidth: 1.5, borderColor: colors.b, backgroundColor: "transparent" },
  btnOutlineText: { color: colors.t, fontSize: 15, fontWeight: "700" },
  disabled: { opacity: 0.4 },
  blob: { backgroundColor: colors.lavL, alignItems: "center", justifyContent: "center", alignSelf: "center", marginBottom: 14 },
  chip: { paddingVertical: 9, paddingHorizontal: 16, borderRadius: 999, borderWidth: 1.5, borderColor: colors.b, backgroundColor: colors.c, marginRight: 8, marginBottom: 8 },
  chipSelected: { borderColor: colors.a, backgroundColor: colors.al },
  chipText: { fontSize: 13, fontWeight: "600", color: colors.t },
  chipTextSelected: { color: colors.ad },
  option: { padding: 16, borderRadius: 14, borderWidth: 1.5, borderColor: colors.b, backgroundColor: colors.c, marginBottom: 10 },
  optionSelected: { borderColor: colors.a, backgroundColor: colors.al },
  optionTitle: { fontSize: 14, fontWeight: "700", color: colors.t },
  optionSubtitle: { fontSize: 12.5, color: colors.ts, marginTop: 2, fontWeight: "400" },
  tag: { paddingVertical: 5, paddingHorizontal: 12, borderRadius: 999, backgroundColor: colors.al, marginRight: 6, marginBottom: 6 },
  tagText: { fontSize: 12, fontWeight: "700", color: colors.ad },
});
