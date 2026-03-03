<script setup>
import {
  Bell,
  Search,
  User,
  Plus
} from "lucide-vue-next";
import { useRoute } from "vue-router";
import { computed } from "vue";

const route = useRoute();

const pathSegments = computed(() =>
  route.path.split("/").filter(Boolean)
);

const role = computed(() => pathSegments.value[0]);

const currentPath = computed(() => {
  const segments = pathSegments.value;

  if (
    segments.length === 0 ||
    segments[segments.length - 1] === "admin" ||
    segments[segments.length - 1] === "doctor"
  ) {
    return "Dashboard";
  }

  return segments[segments.length - 1]
    .replace(/-/g, " ")
    .replace(/\b\w/g, char => char.toUpperCase());
});

console.log("role", role.value);

</script>

<template>
  <nav class="h-20 w-full bg-white border-b border-gray-100 flex items-center justify-between px-8">

    <div class="shrink-0">
      <h1 class="font-bold text-xl text-slate-800 tracking-tight">{{ currentPath }}</h1>
    </div>

    <div class="flex-1 max-w-2xl px-8">
      <div class="relative group">
        <Search
          class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-blue-500 transition-colors"
          :size="18" />
        <input type="text" placeholder="Search by name, ID, or specialization..."
          class="w-full bg-slate-50 border border-slate-200 rounded-xl pl-10 pr-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all" />
      </div>
    </div>


    <div class="flex items-center gap-6">
      <template v-if="currentPath === 'Doctors' || currentPath === 'Patient'">
        <button
          class="flex cursor-pointer items-center gap-2 px-4 py-2.5 bg-blue-600 text-white rounded-xl font-bold text-sm shadow-lg shadow-blue-100 hover:bg-blue-700 transition-all">
          <Plus :size="18" /> Add Dcotor
        </button>
      </template>
      <div class="h-8 w-px bg-slate-100"></div>

      <button class="flex items-center gap-3 group">
        <div
          class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 ring-2 ring-transparent group-hover:ring-blue-100 transition-all">
          <User :size="20" />
        </div>
        <div class="text-left hidden md:block">
          <p class="text-md font-semibold text-slate-800 leading-none">Rahul Sharma</p>
          <template v-if="role === 'doctor'">
            <p class="text-xs text-slate-400 mt-1">Doctor</p>
          </template>
          <template v-else-if="role === 'admin'">
            <p class="text-xs text-slate-400 mt-1">Administrator</p>
          </template>
          <template v-else-if="role === 'patient'">
            <p class="text-xs text-slate-400 mt-1">Patient</p>
          </template>
        </div>
      </button>
    </div>

  </nav>
</template>