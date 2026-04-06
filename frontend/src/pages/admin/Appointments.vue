<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import {
  Calendar as CalendarIcon, ChevronDown, ChevronLeft, ChevronRight,
  Search, User, Activity, X, Loader2
} from 'lucide-vue-next';
import { getAppointment, getDoctorList } from '../../services/admin';
import { useToast } from 'vue-toastification';

const toast = useToast();

// --- State Management ---
const currentView = ref('table');
const appointments = ref([]);
const isLoading = ref(false);
const currentPage = ref(1);
const totalPages = ref(1);
const totalRecords = ref(0);
let searchTimeout = null;

const doctorNameList = ref([]);
const loadDoctor = ref(false);

const today = new Date();
const activeMonth = ref(new Date());

const selectedDoctor = ref('All Doctors');
const searchQuery = ref('');

// --- Data Fetching ---
const fetchAppointments = async () => {
  isLoading.value = true;
  try {
    const isCalendar = currentView.value === 'calendar';
    const params = {
      page: isCalendar ? 1 : currentPage.value,
      limit: isCalendar ? 1000 : 10,
      doctor: selectedDoctor.value === "All Doctors" ? undefined : selectedDoctor.value,
      search: searchQuery.value.trim() || undefined
    };

    const res = await getAppointment(params);
    totalRecords.value = res.total || 0;
    totalPages.value = res.total_pages || 1;
    appointments.value = res.data || [];
  } catch (error) {
    toast.error("Failed to load appointments. Please try again.");
  } finally {
    isLoading.value = false;
  }
};

const fetchDoctor = async () => {
  loadDoctor.value = true;
  try {
    const res = await getDoctorList();
    doctorNameList.value = res.data || [];
  } catch (error) {
    toast.error("Failed to fetch doctor list.");
  } finally {
    loadDoctor.value = false;
  }
};

// --- Watchers ---
watch([searchQuery], () => {
  currentPage.value = 1;
  if (searchTimeout) clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => fetchAppointments(), 400);
});

watch([currentPage, currentView, selectedDoctor], () => fetchAppointments());

onMounted(() => {
  fetchAppointments();
  fetchDoctor();
});

// --- Actions ---
const resetFilters = () => {
  searchQuery.value = '';
  selectedDoctor.value = 'All Doctors';
};

const changeMonth = (step) => {
  const newDate = new Date(activeMonth.value);
  newDate.setMonth(newDate.getMonth() + step);
  activeMonth.value = newDate;
};

// --- Calendar Logic ---
const monthName = computed(() =>
  activeMonth.value.toLocaleString('default', { month: 'long', year: 'numeric' })
);

const calendarDays = computed(() => {
  const year = activeMonth.value.getFullYear();
  const month = activeMonth.value.getMonth();
  const firstDayIndex = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  return [...Array(firstDayIndex).fill(null), ...Array.from({ length: daysInMonth }, (_, i) => i + 1)];
});

const getAptsForDay = (day) => {
  if (!day) return [];
  return appointments.value.filter(a => {
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
    case 'Confirmed': return 'status-active';
    case 'Pending': return 'status-on-leave';
    case 'Cancelled': return 'status-critical';
    default: return 'status-inactive';
  }
};

const getDeptClass = (dept) => {
  const styles = {
    'Cardiology': 'bg-blue-light text-blue',
    'Neurology': 'bg-emerald-light text-emerald',
    'General Medicine': 'bg-orange-light text-orange'
  };
  return styles[dept] || 'bg-slate-50 text-slate-600';
};
</script>

<template>
  <div class="main-wrapper">
    <div class="content-container">
      
      <div class="filter-bar-card">
        <div class="search-input-wrapper">
          <Search class="input-icon-left" :size="18" />
          <input v-model.trim="searchQuery" type="text" placeholder="Search patients..." class="styled-input" />
        </div>

        <div class="filter-divider"></div>

        <div class="dropdown-filter-item">
          <User :size="14" class="icon-muted" />
          <div class="filter-content">
            <span class="mini-label">Doctor</span>
            <select v-model="selectedDoctor" class="ghost-select">
              <option>All Doctors</option>
              <option v-for="doc in doctorNameList" :value="doc.id" :key="doc.id">{{ doc.name }}</option>
            </select>
          </div>
        </div>

        <button @click="resetFilters" class="btn-clear" title="Clear Filters">
          <X :size="18" />
        </button>
      </div>

      <div class="table-card">
        <div v-if="isLoading" class="loader-overlay">
          <Loader2 class="spinner" :size="32" />
          <span class="loader-text">Updating...</span>
        </div>

        <div class="card-view-header">
          <div class="view-title-area">
            <h3 class="view-title">{{ currentView === 'calendar' ? monthName : 'Active Appointments' }}</h3>
            
            <div v-if="currentView === 'calendar'" class="calendar-nav">
              <button @click="changeMonth(-1)" class="nav-btn"><ChevronLeft :size="16" /></button>
              <button @click="activeMonth = new Date()" class="today-link">Today</button>
              <button @click="changeMonth(1)" class="nav-btn"><ChevronRight :size="16" /></button>
            </div>
          </div>

          <div class="view-toggle-bg">
            <button @click="currentView = 'table'" :class="['toggle-btn', {active: currentView === 'table'}]">Table</button>
            <button @click="currentView = 'calendar'" :class="['toggle-btn', {active: currentView === 'calendar'}]">Calendar</button>
          </div>
        </div>

        <div v-if="currentView === 'table'" class="table-scroll">
          <table class="data-table">
            <thead>
              <tr>
                <th class="px-8">Time & Date</th>
                <th>Patient Details</th>
                <th>Assigned Doctor</th>
                <th>Department</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(apt, i) in appointments" :key="i">
                <td class="px-8">
                  <p class="text-bold">{{ apt.time }}</p>
                  <p class="text-muted">{{ apt.date }}</p>
                </td>
                <td>
                  <div class="doc-info-flex">
                    <div class="avatar-circle">{{ (apt.patient_name || '?').charAt(0) }}</div>
                    <div>
                      <p class="doc-name-text">{{ apt.patient_name }}</p>
                      <p class="doc-email-text">{{ apt.patient_id }}</p>
                    </div>
                  </div>
                </td>
                <td><span class="text-medium">{{ apt.doctor_name }}</span></td>
                <td><span :class="['dept-badge', getDeptClass(apt.department)]">{{ apt.department }}</span></td>
                <td>
                  <span :class="['status-pill', getStatusClass(apt.status)]">
                    <span class="dot"></span>{{ apt.status }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
          
          <footer class="table-footer">
            <p class="footer-count">Showing <b>{{ ((currentPage - 1) * 10) + 1 }} - {{ Math.min(currentPage * 10, totalRecords) }}</b> of {{ totalRecords }}</p>
            <div class="pagination-controls">
              <button @click="prevPage" :disabled="currentPage === 1" class="page-arrow"><ChevronLeft :size="18"/></button>
              <button v-for="p in Math.min(3, totalPages)" :key="p" @click="currentPage = p" :class="['page-num', {active: currentPage === p}]">{{ p }}</button>
              <button @click="nextPage" :disabled="currentPage >= totalPages" class="page-arrow"><ChevronRight :size="18"/></button>
            </div>
          </footer>
        </div>

        <div v-else class="calendar-container">
          <div class="calendar-grid">
            <div v-for="dayName in ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']" :key="dayName" class="calendar-header-cell">
              {{ dayName }}
            </div>

            <div v-for="(day, index) in calendarDays" :key="index" :class="['calendar-day-cell', { 'has-day': day }]">
              <div v-if="day" class="day-number-row">
                <span :class="['day-label', { 'is-today': isToday(day) }]">{{ day }}</span>
              </div>
              <div v-if="day" class="day-events scrollbar-hide">
                <div v-for="apt in getAptsForDay(day)" :key="apt.id" class="calendar-event-item">
                  <div class="event-time-row">
                    <span class="event-time">{{ apt.time }}</span>
                    <div :class="['event-dot', getStatusClass(apt.status)]"></div>
                  </div>
                  <p class="event-patient">{{ apt.patient_name }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<style src="../../styles/adminDoctor.css" scoped></style>