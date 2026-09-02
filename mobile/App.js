import React from "react";
import { StatusBar } from "expo-status-bar";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { AuthProvider } from "./src/context/AuthContext";

import LoginScreen from "./src/screens/LoginScreen";
import JoinScreen from "./src/screens/JoinScreen";
import SetupScreen from "./src/screens/SetupScreen";
import MoodScreen from "./src/screens/MoodScreen";
import SceneScreen from "./src/screens/SceneScreen";
import LoadingScreen from "./src/screens/LoadingScreen";
import MatchScreen from "./src/screens/MatchScreen";
import DeclineScreen from "./src/screens/DeclineScreen";
import BuddyScreen from "./src/screens/BuddyScreen";
import GoScreen from "./src/screens/GoScreen";
import ThreadsScreen from "./src/screens/ThreadsScreen";
import ChatScreen from "./src/screens/ChatScreen";
import ReportScreen from "./src/screens/ReportScreen";

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <AuthProvider>
      <NavigationContainer>
        <Stack.Navigator screenOptions={{ headerShown: false }} initialRouteName="Login">
          <Stack.Screen name="Login" component={LoginScreen} />
          <Stack.Screen name="Join" component={JoinScreen} />
          <Stack.Screen name="Setup" component={SetupScreen} />
          <Stack.Screen name="Mood" component={MoodScreen} />
          <Stack.Screen name="Scene" component={SceneScreen} />
          <Stack.Screen name="Loading" component={LoadingScreen} />
          <Stack.Screen name="Match" component={MatchScreen} />
          <Stack.Screen name="Decline" component={DeclineScreen} options={{ presentation: "modal" }} />
          <Stack.Screen name="Buddy" component={BuddyScreen} />
          <Stack.Screen name="Go" component={GoScreen} />
          <Stack.Screen name="Threads" component={ThreadsScreen} />
          <Stack.Screen name="Chat" component={ChatScreen} />
          <Stack.Screen name="Report" component={ReportScreen} options={{ presentation: "modal" }} />
        </Stack.Navigator>
        <StatusBar style="dark" />
      </NavigationContainer>
    </AuthProvider>
  );
}
