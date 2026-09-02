import React from "react";
import { View, Text, StyleSheet } from "react-native";
import { Btn, Blob } from "../ui";
import { colors } from "../theme";

export default function GoScreen({ navigation }) {
  return (
    <View style={styles.screen}>
      <Blob emoji="🎉" size={90} />
      <Text style={styles.title}>Have a beautiful time!</Text>
      <Text style={styles.sub}>We'll check in after your visit.</Text>
      <Btn title="Find another place" onPress={() => navigation.reset({ index: 0, routes: [{ name: "Mood" }] })} />
    </View>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.bg, padding: 24, paddingTop: 100, alignItems: "center" },
  title: { fontSize: 22, fontWeight: "700", color: colors.t, marginBottom: 8 },
  sub: { fontSize: 14, color: colors.ts, marginBottom: 24 },
});
