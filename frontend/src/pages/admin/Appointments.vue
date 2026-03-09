<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import {
  Calendar as CalendarIcon, ChevronDown, ChevronLeft, ChevronRight,
  Search, User, Clock, Loader2
} from 'lucide-vue-next';
import { getAppointment, getDoctorList } from '../../services/admin';

// --- State Management ---
const currentView = ref('table');
const appointments = ref([]);
const isLoading = ref(false);
const currentPage = ref(1)
const totalPages = ref(1)
const totalRecords = ref(0)
let searchTimeout = null;

const doctorNameList = ref([])
const laodDoctor = ref(false)

// Date State
const today = new Date();
const activeMonth = ref(new Date());

// Filter State
const selectedDoctor = ref('All Doctors');
const selectedStatus = ref('All Status');
const searchQuery = ref('');

// --- Data Fetching ---
const fetchAppointments = async () => {
  isLoading.value = true;
  try {
    const isCalendar = currentView.value === 'calendar';
    const limit = isCalendar ? 1000 : 10;
    const page = isCalendar ? 1 : currentPage.value;

    const params = {
      page,
      limit,
      doctor: selectedDoctor.value === "All Doctors" ? undefined : selectedDoctor,
      search: searchQuery.value
    }

    const res = await getAppointment(params)

    totalRecords.value = res.total;
    totalPages.value = res.total_pages;
    appointments.value = res.data || [];
  } catch (error) {
    console.error("Fetch error:", error.message);
  } finally {
    isLoading.value = false;
  }
}

const fetchDoctor = async () => {
  laodDoctor.value = true;
  try {
    const res = await getDoctorList();
    doctorNameList.value = res.data
  } catch (error) {
    console.error("Doctor Fetch error:", error.message)
  } finally {
    laodDoctor.value = false
  }
}

// --- Watchers ---

// Watch for page changes (Table pagination)
watch(currentPage, () => {
  if (currentView.value === 'table') {
    fetchAppointments();
  }
});

// Watch for view changes (Table <-> Calendar)
watch(currentView, () => {
  currentPage.value = 1;
  fetchAppointments();
});

// Watch for month changes in Calendar
watch(activeMonth, () => {
  if (currentView.value === 'calendar') {
    fetchAppointments();
  }
});

watch([searchQuery], () => {
  currentPage.value = 1 // Reset to page 1 on filter change
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    fetchAppointments()
  }, 400)
})

// --- Pagination ---
const nextPage = () => { if (currentPage.value < totalPages.value) currentPage.value++ }
const prevPage = () => { if (currentPage.value > 1) currentPage.value-- }

// --- Computed Filter Logic ---
const doctorsList = computed(() => {
  const names = appointments.value.map(a => a.doctor_name);
  return ['All Doctors', ...new Set(names)];
});

const statusList = ['All Status', 'Confirmed', 'Pending', 'Cancelled'];

const filteredAppointments = computed(() => {
  return appointments.value.filter(apt => {
    const doctorMatch = selectedDoctor.value === 'All Doctors' || apt.doctor_name === selectedDoctor.value;
    const statusMatch = selectedStatus.value === 'All Status' || apt.status === selectedStatus.value;
    return doctorMatch && statusMatch;
  });
});

// --- Calendar Math & Logic ---
const monthName = computed(() =>
  activeMonth.value.toLocaleString('default', { month: 'long', year: 'numeric' })
);

const calendarDays = computed(() => {
  const year = activeMonth.value.getFullYear();
  const month = activeMonth.value.getMonth();

  const firstDayIndex = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  const padding = Array(firstDayIndex).fill(null);
  const days = Array.from({ length: daysInMonth }, (_, i) => i + 1);

  return [...padding, ...days];
});

const changeMonth = (step) => {
  const newDate = new Date(activeMonth.value);
  newDate.setMonth(newDate.getMonth() + step);
  activeMonth.value = newDate;
};

const getAptsForDay = (day) => {
  if (!day) return [];
  return filteredAppointments.value.filter(a => {
    const aptDate = new Date(a.date);
    return aptDate.getDate() === day &&
      aptDate.getMonth() === activeMonth.value.getMonth() &&
      aptDate.getFullYear() === activeMonth.value.getFullYear();
  });
};

const isToday = (day) => {
  return day === today.getDate() &&
    activeMonth.value.getMonth() === today.getMonth() &&
    activeMonth.value.getFullYear() === today.getFullYear();
};

// --- Style Helpers ---
const getStatusClass = (status) => {
  switch (status) {
    case 'Confirmed': return 'text-emerald-500 bg-emerald-500';
    case 'Pending': return 'text-amber-500 bg-amber-500';
    case 'Cancelled': return 'text-slate-400 bg-slate-400';
    default: return 'text-blue-500 bg-blue-500';
  }
};

const getDeptClass = (dept) => {
  const styles = {
    'Cardiology': 'bg-blue-50 text-blue-600',
    'Neurology': 'bg-purple-50 text-purple-600',
    'General Medicine': 'bg-orange-50 text-orange-600'
  };
  return styles[dept] || 'bg-slate-50 text-slate-600';
};

// --- Initial Load ---
onMounted(() => {
  fetchAppointments();
  fetchDoctor()
});

</script>

<template>
  <div class="p-8 bg-slate-50 min-h-screen font-sans">

    <div class="bg-white p-2 rounded-2xl border border-slate-200 shadow-sm mb-8 flex items-center gap-2 flex-wrap">

      <div class="relative flex-1 min-w-75">
        <Search class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" :size="18" />
        <input v-model.trim="searchQuery" type="text" placeholder="Search patients..."
          class="w-full bg-white border border-slate-200 rounded-xl pl-10 pr-4 py-2.5 text-sm font-medium text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all shadow-sm" />
      </div>

      <div class="hidden md:block h-8 w-px bg-slate-100 mx-2"></div>

      <div
        class="flex items-center gap-2 px-3 py-1.5 bg-slate-50 rounded-xl border border-slate-100 hover:border-slate-200 transition-all">
        <User :size="14" class="text-slate-400" />
        <div class="flex flex-col">
          <span class="text-[9px] font-bold text-slate-400 uppercase tracking-tight">Doctor</span>
          <select v-model="selectedDoctor"
            class=" rounded-xl text-sm cursor-pointer font-medium text-slate-700 focus:outline-none">
            <option default>All Doctors</option>
            <option v-for="doc in doctorNameList" :key="doc.id">{{ doc.name }}</option>
          </select>
        </div>
      </div>

      <div
        class="flex items-center gap-2 px-3 py-1.5 bg-slate-50 rounded-xl border border-slate-100 hover:border-slate-200 transition-all">
        <Activity :size="14" class="text-slate-400" />
        <div class="flex flex-col">
          <span class="text-[9px] font-bold text-slate-400 uppercase tracking-tight">Status</span>
          <select v-model="selectedStatus"
            class=" rounded-xl cursor-pointer text-sm font-medium text-slate-700 focus:outline-none">
            <option v-for="st in statusList" :key="st">{{ st }}</option>
          </select>
        </div>
      </div>

      <button @click="resetFilters"
        class="p-3 text-slate-400 hover:text-red-500 hover:bg-red-50 rounded-xl transition-all" title="Clear Filters">
        <X :size="18" />
      </button>
    </div>

    <div class="bg-white rounded-3xl border border-slate-100 shadow-sm overflow-hidden relative">

      <div class="p-6 border-b border-slate-50 flex items-center justify-between">
        <div class="flex items-center gap-4">
          <h3 class="font-bold text-slate-800 text-lg">
            {{ currentView === 'calendar' ? monthName : 'Active Appointments' }}
          </h3>

          <div v-if="currentView === 'calendar'" class="flex items-center gap-2 ml-4">
            <button @click="changeMonth(-1)"
              class="p-1.5 hover:bg-slate-100 rounded-lg transition-colors text-slate-400">
              <ChevronLeft :size="16" />
            </button>
            <button @click="activeMonth = new Date()"
              class="text-[10px] font-bold uppercase text-blue-600 hover:text-blue-700 px-2">Today</button>
            <button @click="changeMonth(1)"
              class="p-1.5 hover:bg-slate-100 rounded-lg transition-colors text-slate-400">
              <ChevronRight :size="16" />
            </button>
          </div>
        </div>

        <div class="flex bg-slate-100 p-1 rounded-xl">
          <button @click="currentView = 'table'"
            :class="[currentView === 'table' ? 'bg-white shadow-sm text-slate-800' : 'text-slate-400']"
            class="px-5 py-1.5 text-xs font-bold rounded-lg transition-all">Table</button>
          <button @click="currentView = 'calendar'"
            :class="[currentView === 'calendar' ? 'bg-white shadow-sm text-slate-800' : 'text-slate-400']"
            class="px-5 py-1.5 text-xs font-bold rounded-lg transition-all">Calendar</button>
        </div>
      </div>

      <div v-if="currentView === 'table'" class="overflow-x-auto">
        <table class="w-full text-left">
          <thead>
            <tr class="text-[10px] font-bold text-slate-400 uppercase tracking-[0.15em] border-b border-slate-50">
              <th class="px-8 py-5">Time & Date</th>
              <th class="px-8 py-5">Patient Details</th>
              <th class="px-8 py-5">Assigned Doctor</th>
              <th class="px-8 py-5">Department</th>
              <th class="px-8 py-5">Status</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-50">
            <tr v-for="(apt, i) in filteredAppointments" :key="i" class="hover:bg-slate-50/50 transition-colors">
              <td class="px-8 py-5">
                <p class="font-bold text-slate-800 text-sm">{{ apt.time }}</p>
                <p class="text-[11px] text-slate-400">{{ apt.date }}</p>
              </td>
              <td class="px-8 py-5">
                <div class="flex items-center gap-3">
                  <div
                    class="w-9 h-9 rounded-full bg-blue-50 flex items-center justify-center text-[11px] font-bold text-blue-500 border border-blue-100 uppercase">
                    {{ (apt.patient_name || '?').charAt(0) }}
                  </div>
                  <div>
                    <p class="font-bold text-slate-800 text-sm">{{ apt.patient_name }}</p>
                    <p class="text-[11px] text-slate-400">{{ apt.patient_id }}</p>
                  </div>
                </div>
              </td>
              <td class="px-8 py-5">
                <span class="text-sm font-medium text-slate-600">{{ apt.doctor_name }}</span>
              </td>
              <td class="px-8 py-5">
                <span
                  :class="[getDeptClass(apt.department), 'px-3 py-1 rounded-full text-[10px] font-bold uppercase']">{{
                    apt.department }}</span>
              </td>
              <td class="px-8 py-5">
                <div class="flex items-center gap-2">
                  <span class="w-2 h-2 rounded-full" :class="getStatusClass(apt.status)"></span>
                  <span class="text-sm font-bold capitalize" :class="getStatusClass(apt.status).split(' ')[0]">{{
                    apt.status }}</span>
                </div>
              </td>
            </tr>
            <tr v-if="filteredAppointments.length === 0 && !isLoading">
              <td colspan="5" class="py-20 text-center text-slate-400 text-sm italic">No appointments found matching
                these filters.</td>
            </tr>
          </tbody>
        </table>
        <div class="px-6 py-4 border-t border-slate-100 flex items-center justify-between bg-white">
          <div class="text-sm text-slate-500">
            Showing <span class="font-bold text-slate-800">{{ ((currentPage - 1) * 10) + 1 }} to {{ Math.min(currentPage
              *
              10, totalRecords) }}</span> of <span class="font-bold text-slate-800">{{ totalRecords }}</span> patients
          </div>
          <div class="flex items-center gap-2">
            <button @click="prevPage" :disabled="currentPage === 1"
              class="p-2 rounded-lg border border-slate-200 text-slate-400 hover:bg-slate-50 disabled:opacity-30 transition-all">
              <ChevronLeft :size="18" />
            </button>
            <div class="flex items-center gap-1">
              <button v-for="p in Math.min(3, totalPages)" :key="p" @click="currentPage = p"
                :class="['px-3.5 py-1.5 text-sm font-bold rounded-lg transition-all', currentPage === p ? 'bg-blue-600 text-white' : 'text-slate-500 hover:bg-slate-50']">
                {{ p }}
              </button>
            </div>
            <button @click="nextPage" :disabled="currentPage >= totalPages"
              class="p-2 rounded-lg border border-slate-200 text-slate-400 hover:bg-slate-50 disabled:opacity-30 transition-all">
              <ChevronRight :size="18" />
            </button>
          </div>
        </div>
      </div>

      <div v-else class="p-6">
        <div class="grid grid-cols-7 border-t border-l border-slate-100">
          <div v-for="dayName in ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']" :key="dayName"
            class="p-3 text-center text-[10px] font-bold text-slate-400 uppercase tracking-widest border-r border-b border-slate-100 bg-slate-50/50">
            {{ dayName }}
          </div>

          <div v-for="(day, index) in calendarDays" :key="index"
            :class="['min-h-32 p-2 border-r border-b border-slate-100 transition-colors relative', day ? 'hover:bg-slate-50/30' : 'bg-slate-50/10']">

            <div v-if="day" class="mb-2">
              <span
                :class="['text-xs font-bold w-6 h-6 flex items-center justify-center rounded-full', isToday(day) ? 'bg-blue-600 text-white' : 'text-slate-300']">
                {{ day }}
              </span>
            </div>

            <div v-if="day" class="space-y-1.5 overflow-y-auto max-h-24 scrollbar-hide">
              <div v-for="apt in getAptsForDay(day)" :key="apt.patient_id"
                class="p-1.5 rounded-lg border border-blue-100 bg-blue-50/50 hover:bg-blue-100/50 transition-all cursor-pointer">
                <div class="flex items-center justify-between gap-1 mb-0.5">
                  <p class="text-[8px] font-bold text-blue-700 uppercase">{{ apt.time }}</p>
                  <div class="w-1.5 h-1.5 rounded-full" :class="getStatusClass(apt.status)"></div>
                </div>
                <p class="text-[10px] font-bold text-slate-700 truncate">{{ apt.patient_name }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="isLoading"
        class="absolute inset-0 bg-white/60 backdrop-blur-[1px] flex items-center justify-center z-50">
        <div class="flex flex-col items-center gap-2">
          <Loader2 class="animate-spin text-blue-600" :size="32" />
          <span class="text-xs font-bold text-slate-500 uppercase tracking-widest">Updating...</span>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}

.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>