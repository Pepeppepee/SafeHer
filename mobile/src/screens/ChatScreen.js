import React, { useEffect, useRef, useState } from "react";
import { View, Text, TextInput, TouchableOpacity, StyleSheet, FlatList, KeyboardAvoidingView, Platform } from "react-native";
import { api } from "../api";
import { colors } from "../theme";

export default function ChatScreen({ route, navigation }) {
  const { threadId } = route.params;
  const [thread, setThread] = useState(null);
  const [text, setText] = useState("");
  const pollRef = useRef(null);

  async function load() {
    const r = await api(`/api/buddies/threads/${threadId}/`);
    if (r.ok) setThread(r.data);
  }

  useEffect(() => {
    load();
    pollRef.current = setInterval(load, 4000);
    return () => clearInterval(pollRef.current);
  }, [threadId]);

  async function send() {
    const v = text.trim();
    if (!v) return;
    const r = await api(`/api/buddies/threads/${threadId}/messages/`, { content: v });
    if (r.ok) { setText(""); load(); }
    else alert(r.data.content?.[0] || r.data.error || "Message couldn't be sent");
  }

  if (!thread) return <View style={styles.screen} />;

  return (
    <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : undefined} style={styles.screen}>
      <View style={styles.header}>
        <View style={{ flex: 1 }}>
          <Text style={styles.headerTitle}>{thread.experience_name}</Text>
          <Text style={styles.headerSub}>{thread.members.length} women · trip on {thread.trip_date}</Text>
        </View>
        <TouchableOpacity onPress={() => navigation.navigate("Report", { threadId, members: thread.members })}>
          <Text style={styles.report}>🚩</Text>
        </TouchableOpacity>
      </View>
      <FlatList
        data={thread.messages}
        keyExtractor={(m) => m.id}
        contentContainerStyle={{ padding: 12 }}
        renderItem={({ item }) => (
          <View style={[styles.bubble, item.is_me ? styles.bubbleMe : styles.bubbleThem]}>
            {!item.is_me ? <Text style={styles.sender}>{item.sender_name}</Text> : null}
            <Text style={item.is_me ? styles.bubbleTextMe : styles.bubbleText}>{item.content}</Text>
          </View>
        )}
        ListEmptyComponent={<Text style={styles.empty}>This chat is just getting started.{"\n"}Say hi 👋</Text>}
      />
      <View style={styles.inputRow}>
        <TextInput style={styles.input} placeholder="Say something kind..." value={text} onChangeText={setText} onSubmitEditing={send} />
        <TouchableOpacity style={styles.sendBtn} onPress={send}><Text style={{ color: "#fff", fontSize: 16 }}>➤</Text></TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.bg },
  header: { flexDirection: "row", alignItems: "center", padding: 16, paddingTop: 40 },
  headerTitle: { fontSize: 16, fontWeight: "700", color: colors.t },
  headerSub: { fontSize: 12, color: colors.ts },
  report: { fontSize: 18 },
  bubble: { maxWidth: "78%", padding: 10, borderRadius: 16, marginBottom: 8 },
  bubbleMe: { backgroundColor: colors.a, alignSelf: "flex-end", borderBottomRightRadius: 4 },
  bubbleThem: { backgroundColor: colors.c, alignSelf: "flex-start", borderBottomLeftRadius: 4, elevation: 1 },
  bubbleText: { color: colors.t, fontSize: 13.5 },
  bubbleTextMe: { color: "#fff", fontSize: 13.5 },
  sender: { fontSize: 10.5, fontWeight: "700", opacity: 0.6, marginBottom: 2, color: colors.t },
  empty: { textAlign: "center", color: colors.tm, marginTop: 60 },
  inputRow: { flexDirection: "row", padding: 12, gap: 8 },
  input: { flex: 1, backgroundColor: colors.c, borderRadius: 14, paddingHorizontal: 14, paddingVertical: 10 },
  sendBtn: { width: 44, height: 44, borderRadius: 22, backgroundColor: colors.a, alignItems: "center", justifyContent: "center" },
});
