import { defineStore } from "pinia";
import { ref, computed } from "vue";

export const useUserStore = defineStore("user", () => {
  // State
  const user = ref(null);
  const token = ref(localStorage.getItem("token") || null);

  // Getters
  const isLoggedIn = computed(() => !!user.value && !!token.value);
  
  const userInitials = computed(() => {
    if (!user.value?.name) return "??";
    return user.value.name
      .split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase();
  });

  // Actions
  function setUser(userData, authToken) {
    user.value = userData;
    token.value = authToken;
    localStorage.setItem("token", authToken);
  }

  function clearUser() {
    user.value = null;
    token.value = null;
    localStorage.removeItem("token");
  }

  return { user, token, isLoggedIn, userInitials, setUser, clearUser };
}, 
{
  persist: true 
});