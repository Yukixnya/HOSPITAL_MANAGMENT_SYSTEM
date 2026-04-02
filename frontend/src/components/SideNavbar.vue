<script setup>
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { 
  LayoutGrid, BriefcaseMedical, Users, 
  CalendarDays, LogOut, TimerReset
} from 'lucide-vue-next';
import { useUserStore } from '../store/userStore';

const route = useRoute();
const router = useRouter();
const userStore = useUserStore();

const currentRole = computed(() => {
  const segments = route.path.split('/').filter(Boolean);
  return segments[0] || 'patient';
});

const isActive = (link) => {
  if (link === '/' + currentRole.value) {
    return route.path === link;
  }
  return route.path.startsWith(link);
};

const menuGroups = {
  admin: [
    { name: 'Dashboard', icon: LayoutGrid, link: '/admin' },
    { name: 'Doctors', icon: BriefcaseMedical, link: '/admin/doctors' },
    { name: 'Patients', icon: Users, link: '/admin/patients' },
    { name: 'Appointments', icon: CalendarDays, link: '/admin/appointments' }
  ],
  doctor: [
    { name: 'Dashboard', icon: LayoutGrid, link: '/doctor' },
    { name: 'My Patients', icon: Users, link: '/doctor/patients' },
    { name: 'Appointments', icon: CalendarDays, link: '/doctor/appointments' }
  ],
  patient: [
    { name: 'Dashboard', icon: LayoutGrid, link: '/patient' },
    { name: 'My Doctors', icon: Users, link: '/patient/doctors' },
    { name: 'Appointments', icon: CalendarDays, link: '/patient/my-appointments' },
    { name: "Medical History", icon: TimerReset, link: '/patient/medical-history' }
  ]
};

const currentMenu = computed(() => menuGroups[currentRole.value] || menuGroups.patient);

const handleLogout = () => {
  userStore.clearUser();
  router.push('/auth/login');
};
</script>

<template>
  <aside class="sidebar">
    <div class="sidebar-brand">
      <div class="brand-logo">
        <svg viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 2L4 5v6.09c0 5.05 3.41 9.76 8 10.91 4.59-1.15 8-5.86 8-10.91V5l-8-3zm1 14h-2v-3H8v-2h3V8h2v3h3v2h-3v3z"/>
        </svg>
      </div>
      <div class="brand-text">
        <h1 class="brand-name">MedCore</h1>
        <p class="brand-tagline">Enterprise Portal</p>
      </div>
    </div>

    <nav class="sidebar-nav">
      <button
        v-for="item in currentMenu"
        :key="item.name"
        @click="$router.push(item.link)"
        :class="['nav-link', { 'is-active': isActive(item.link) }]"
      >
        <component 
          :is="item.icon" 
          class="nav-icon" 
          :stroke-width="isActive(item.link) ? 2.5 : 2" 
        />
        <span class="nav-label">{{ item.name }}</span>
      </button>
    </nav>

    <footer class="sidebar-footer">
      <button @click="handleLogout" class="nav-link is-danger">
        <LogOut class="nav-icon" />
        <span class="nav-label">Logout</span>
      </button>
    </footer>
  </aside>
</template>

<style src="./styles/sidebar.css" scoped></style>