<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import {
  CalendarIcon, UsersIcon, ClipboardIcon,
  ClockIcon, ChevronRightIcon, SearchIcon, FilterIcon
} from 'lucide-vue-next';
import { getDoctorDashboard } from '../../services/doctor';
import { useToast } from 'vue-toastification';

const toast = useToast();
const router = useRouter();
const recentPatients = ref([]);
const selectedDate = ref(new Date().toISOString().split('T')[0]);

const dashboard = ref({
  "appointments": [],
  "pending_reports": 0,
  "today_appointments": 0,
  "total_patients": 0,
});

const dynamicDays = computed(() => {
  const days = [];
  const today = new Date();
  for (let i = 0; i < 7; i++) {
    const date = new Date();
    date.setDate(today.getDate() + i);
    days.push({
      name: date.toLocaleDateString('en-US', { weekday: 'short' }),
      dateNum: date.getDate(),
      isoDate: date.toISOString().split('T')[0]
    });
  }
  return days;
});

const filteredAppointments = computed(() => {
  return dashboard.value.appointments
    .filter(appt => appt.date === selectedDate.value)
    .sort((a, b) => a.time.localeCompare(b.time));
});

const goToAppointment = (id) => router.push(`/appointment/${id}`);

const doctorDashboard = async () => {
  try {
    const res = await getDoctorDashboard();
    recentPatients.value = res.recent_patients || [];
    dashboard.value = res;
  } catch (error) { 
    toast.error('Failed to load dashboard data. Please try again later.');
  } 
};

onMounted(doctorDashboard);
</script>

<template>
  <div class="min-h-screen bg-[#f8fafc] p-4 lg:p-8 font-sans text-slate-700">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200/60 flex items-center gap-5">
        <div class="p-4 bg-blue-50 text-blue-600 rounded-xl">
          <CalendarIcon class="w-6 h-6" />
        </div>
        <div>
          <p class="text-sm font-medium text-slate-500 uppercase tracking-wider">Today's Schedule</p>
          <p class="text-3xl font-bold text-slate-900">{{ dashboard.today_appointments }} <span
              class="text-sm font-normal text-slate-400">Slots</span></p>
        </div>
      </div>
      <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200/60 flex items-center gap-5">
        <div class="p-4 bg-emerald-50 text-emerald-600 rounded-xl">
          <UsersIcon class="w-6 h-6" />
        </div>
        <div>
          <p class="text-sm font-medium text-slate-500 uppercase tracking-wider">Total Patients</p>
          <p class="text-3xl font-bold text-slate-900">{{ dashboard.total_patients }}</p>
        </div>
      </div>
      <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200/60 flex items-center gap-5">
        <div class="p-4 bg-orange-50 text-orange-600 rounded-xl">
          <ClipboardIcon class="w-6 h-6" />
        </div>
        <div>
          <p class="text-sm font-medium text-slate-500 uppercase tracking-wider">Pending Action</p>
          <p class="text-3xl font-bold text-slate-900">{{ dashboard.pending_reports || 0 }}</p>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
      <div class="lg:col-span-8 space-y-6">
        <div class="bg-white rounded-3xl shadow-sm border border-slate-200/60 overflow-hidden">
          <div class="p-6 border-b border-slate-50 flex flex-col md:flex-row md:items-center justify-between gap-4">
            <h2 class="text-xl font-bold text-slate-800">Appointment Planner</h2>
            <div class="flex gap-2 overflow-x-auto pb-2 no-scrollbar">
              <button v-for="day in dynamicDays" :key="day.isoDate" @click="selectedDate = day.isoDate"
                :class="selectedDate === day.isoDate ? 'bg-blue-600 text-white shadow-md shadow-blue-200' : 'bg-slate-50 text-slate-500 hover:bg-slate-100'"
                class="flex flex-col items-center justify-center min-w-13.5 h-16 rounded-2xl transition-all duration-200 shrink-0">
                <span class="text-[10px] font-bold uppercase">{{ day.name }}</span>
                <span class="text-lg font-black">{{ day.dateNum }}</span>
              </button>
            </div>
          </div>

          <div class="p-6">
            <div v-if="filteredAppointments.length > 0" class="space-y-4">
              <div v-for="appt in filteredAppointments" :key="appt._id" @click="goToAppointment(appt._id)"
                class="group flex items-center gap-6 p-4 rounded-2xl border border-slate-100 hover:border-blue-200 hover:bg-blue-50/30 transition-all cursor-pointer">
                <div
                  class="flex flex-col items-center justify-center min-w-17.5 py-2 border-r border-slate-100 group-hover:border-blue-100">
                  <span class="text-sm font-bold text-slate-900">{{ appt.time }}</span>
                  <span class="text-[10px] font-medium text-slate-400 uppercase tracking-tighter">Start</span>
                </div>

                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-2 mb-1">
                    <h3 class="font-bold text-slate-800 truncate">{{ appt.patient_name }}</h3>
                    <span class="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wide"
                      :class="appt.status === 'Confirmed' ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'">
                      {{ appt.status }}
                    </span>
                  </div>
                  <div class="flex items-center gap-3 text-xs text-slate-500 font-medium">
                    <span class="flex items-center gap-1">
                      <UsersIcon class="w-3 h-3" /> {{ appt.patient_age }}y, {{ appt.patient_gender }}
                    </span>
                    <span class="flex items-center gap-1 text-blue-600">
                      <ClockIcon class="w-3 h-3" /> {{ appt.type }}
                    </span>
                  </div>
                </div>

                <ChevronRightIcon
                  class="w-5 h-5 text-slate-300 group-hover:text-blue-500 group-hover:translate-x-1 transition-all" />
              </div>
            </div>

            <div v-else class="flex flex-col items-center justify-center py-20 text-slate-400">
              <div class="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mb-4">
                <CalendarIcon class="w-8 h-8 text-slate-200" />
              </div>
              <p class="font-medium">No appointments scheduled for this day</p>
              <p class="text-xs">Select another date from the header above</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 🔹 SIDEBAR -->
      <div class="w-full lg:w-80 space-y-6">
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
          <h2 class="text-lg font-bold mb-6">Recent Patients</h2>
          <div v-if="recentPatients.length === 0" class="py-10 text-center text-gray-400 text-sm">
            No recent activity
          </div>
          <div v-else class="space-y-4">
            <div v-for="p in recentPatients" :key="p._id"
              class="flex items-center gap-3 p-3 border border-gray-50 rounded-xl hover:bg-gray-50 transition-colors">
              <div
                class="h-10 w-10 bg-blue-100 flex items-center justify-center rounded-full text-blue-600 text-xs font-bold shrink-0">
                {{ p.name?.charAt(0) }}
              </div>
              <div class="min-w-0">
                <p class="text-sm font-bold truncate">
                  {{ p.name }}
                </p>
                <p class="text-[10px] text-gray-400 uppercase tracking-tighter">
                  {{ p.gender }}, {{ p.age }}y
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}

.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>