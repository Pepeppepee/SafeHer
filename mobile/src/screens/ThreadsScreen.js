import React, { useEffect, useState, useCallback } from "react";
import { View, Text, StyleSheet, FlatList, TouchableOpacity } from "react-native";
import { useFocusEffect } from "@react-navigation/native";
import { api } from "../api";
import { colors } from "../theme";

export default function ThreadsScreen({ navigation }) {
  const [threads, setThreads] = useState([]);
  const [loaded, setLoaded] = useState(false);

  useFocusEffect(
    useCallback(() => {
      api("/api/buddies/threads/").then((r) => {
        if (r.ok) setThreads(r.data);
        setLoaded(true);
      });
    }, [])
  );

  return (
    <View style={styles.screen}>
      <Text style={styles.title}>My buddies 👭</Text>
      {loaded && threads.length === 0 ? (
        <Text style={styles.empty}>No active buddy chats yet.{"\n"}Say yes to a buddy match after your next "I'm going" to start one.</Text>
      ) : (
        <FlatList
          data={threads}
          keyExtractor={(t) => t.id}
          renderItem={({ item }) => (
            <TouchableOpacity style={styles.card} onPress={() => navigation.navigate("Chat", { threadId: item.id })}>
              <Text style={styles.cardTitle}>{item.experience_name}</Text>
              <Text style={styles.cardSub}>{item.experience_area} · {item.trip_date}</Text>
              {item.last_message ? (
                <Text style={styles.cardMsg} numberOfLines={1}>{item.last_message.sender_name}: "{item.last_message.content}"</Text>
              ) : (
                <Text style={styles.cardMsg}>Say hi to break the ice 👋</Text>
              )}
              <Text style={styles.cardCount}>{item.member_count} women in this chat</Text>
            </TouchableOpacity>
          )}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.bg, padding: 20 },
  title: { fontSize: 22, fontWeight: "700", color: colors.t, marginBottom: 16 },
  empty: { color: colors.tm, textAlign: "center", marginTop: 60, lineHeight: 20 },
  card: { backgroundColor: colors.c, borderRadius: 16, padding: 14, marginBottom: 10, elevation: 2 },
  cardTitle: { fontWeight: "700", fontSize: 14.5, color: colors.t },
  cardSub: { fontSize: 12, color: colors.tm, marginTop: 2, marginBottom: 6 },
  cardMsg: { fontSize: 12.5, color: colors.ts, backgroundColor: colors.bg, borderRadius: 8, padding: 8 },
  cardCount: { fontSize: 11, color: colors.sageD, backgroundColor: colors.sageL, alignSelf: "flex-start", paddingVertical: 3, paddingHorizontal: 8, borderRadius: 999, marginTop: 8 },
});
