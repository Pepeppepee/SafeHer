// Matches the web app's palette (templates/app.html :root variables) so the
// mobile app feels like the same product, not a reskin.
export const colors = {
  a: "#F0728A", ad: "#C94F63", al: "#FFE9EE",       // rose — primary / CTAs
  sage: "#6FA37F", sageD: "#3F6B4E", sageL: "#E9F5EC", // safety / trust
  lav: "#8B7FC7", lavD: "#5B4F94", lavL: "#EFEBFA",   // accents
  peach: "#E8935B", peachD: "#A85E2E", peachL: "#FDECDD",
  t: "#2E2233", ts: "#6E6275", tm: "#A79CAE",
  b: "#F2E4E9", c: "#FFFFFF", bg: "#FFF8F5",
};

export const sceneTheme = {
  peace: { a: colors.a, ad: colors.ad, al: colors.al },
  energy: { a: "#F0784A", ad: "#B8451A", al: "#FFE7D9" },
  wonder: { a: "#2FA093", ad: "#1C6A60", al: "#DCF3EF" },
  reset: { a: "#4F97D9", ad: "#2A6493", al: "#E1F0FB" },
  cozy: { a: "#D89638", ad: "#8B6914", al: "#FBEEDA" },
};

export const SCENE_META = {
  mainstream: { emoji: "🏛️", label: "Mainstream landmark" },
  hidden_gem: { emoji: "💎", label: "Hidden gem" },
  cafe_social: { emoji: "☕", label: "Café & social" },
};

export const SAFE_META = {
  transport: { icon: "🚕", label: "Getting there" },
  accommodation: { icon: "🏡", label: "Where to stay" },
  area_safety: { icon: "🌙", label: "After dark" },
  connectivity: { icon: "📶", label: "Signal" },
  local_attitude: { icon: "💬", label: "Local vibe" },
  emergency: { icon: "🚨", label: "Emergency" },
  return_route: { icon: "🔁", label: "Getting back" },
};
export const SAFE_ORDER = ["transport", "area_safety", "local_attitude", "connectivity", "return_route", "accommodation", "emergency"];
