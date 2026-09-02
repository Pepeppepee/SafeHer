import React from "react";
import { View, Text, ActivityIndicator, StyleSheet } from "react-native";
import { colors } from "../theme";

export default function LoadingScreen() {
  return (
    <View style={styles.screen}>
      <ActivityIndicator size="large" color={colors.a} />
      <Text style={styles.text}>Finding your perfect place...</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.bg, alignItems: "center", justifyContent: "center" },
  text: { marginTop: 16, color: colors.ts, fontWeight: "600" },
});
