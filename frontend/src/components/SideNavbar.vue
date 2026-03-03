<script setup>
import { ref } from 'vue';
import { 
  LayoutGrid, 
  BriefcaseMedical, 
  Users, 
  CalendarDays, 
  Settings, 
  LogOut 
} from 'lucide-vue-next';
import { useRouter } from 'vue-router';
import { computed} from 'vue';

const router = useRouter();
const route = computed(() => {
  const path = router.currentRoute.value.path.split('/').filter(Boolean);
  return { path };
});

const currentPath = route.value.path[0];

const activeItem = ref('Dashboard');

const AdminMenuItems = [
  { name: 'Dashboard', icon: LayoutGrid, link: '/admin' },
  { name: 'Doctors', icon: BriefcaseMedical, link: '/admin/doctors' },
  { name: 'Patients', icon: Users, link: '/admin/patients' },
  { name: 'Appointments', icon: CalendarDays, link: '/admin/appointments' }
];

const DoctorMenuItems = [
  { name: 'Dashboard', icon: LayoutGrid, link: '/doctor' },
  { name: 'MyPatients', icon: Users, link: '/doctor/patients' },
  { name: 'Appointments', icon: CalendarDays, link: '/doctor/appointments' }
];

const footerItems = [
  { name: 'Settings', icon: Settings },
  { name: 'Logout', icon: LogOut, variant: 'danger' },
];
</script>

<template>
  <aside class="flex flex-col fixed w-64 h-screen bg-white border-r border-gray-100 p-4">
    <div class="flex items-center gap-3 px-2 mb-8">
      <div class="bg-blue-600 p-2 rounded-xl">
        <svg class="w-6 h-6 text-white" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2L4 5v6.09c0 5.05 3.41 9.76 8 10.91 4.59-1.15 8-5.86 8-10.91V5l-8-3zm1 14h-2v-3H8v-2h3V8h2v3h3v2h-3v3z"/>
        </svg>
      </div>
      <div>
        <h1 class="font-bold text-slate-800 leading-tight text-lg">MedCore</h1>
        <p class="text-xs text-slate-400 font-medium">Enterprise Portal</p>
      </div>
    </div>

    <nav class="flex-1 space-y-1">
    <!-- Menu Items -->
     <template v-if="currentPath === 'admin' ? AdminMenuItems : DoctorMenuItems">
       <button
        v-for="item in currentPath === 'admin' ? AdminMenuItems : DoctorMenuItems"
        :key="item.name"
        @click="activeItem = item.name; $router.push(item.link)"
        :class="[
          'w-full cursor-pointer flex items-center gap-4 px-4 py-3 rounded-lg transition-colors duration-200',
          activeItem === item.name 
            ? 'bg-blue-50 text-blue-600' 
            : 'text-slate-500 hover:bg-slate-50 hover:text-slate-700'
        ]"
      >
        <component :is="item.icon" :size="20" :stroke-width="activeItem === item.name ? 2.5 : 2" />
        <span class="font-medium">{{ item.name }}</span>
      </button>
     </template> 
    </nav>

    <div class="pt-4 border-t border-gray-50 space-y-1">
      <button
        v-for="item in footerItems"
        :key="item.name"
        :class="[
          'w-full flex items-center gap-4 px-4 py-3 rounded-lg transition-colors',
          item.variant === 'danger' 
            ? 'text-red-500 hover:bg-red-50' 
            : 'text-slate-500 hover:bg-slate-50'
        ]"
      >
        <component :is="item.icon" :size="20" />
        <span class="font-medium">{{ item.name }}</span>
      </button>
    </div>
  </aside>
</template>