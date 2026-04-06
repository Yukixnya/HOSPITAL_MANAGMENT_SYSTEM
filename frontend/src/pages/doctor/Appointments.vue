<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import {
  HistoryIcon,
  StethoscopeIcon, CheckCircleIcon, XCircleIcon, SearchIcon
} from 'lucide-vue-next';
import { useRouter } from 'vue-router';
import { confirmAppointment, getAppointments, cancelAppointment } from '../../services/doctor';
import { useToast } from 'vue-toastification';

const toast = useToast();
const router = useRouter();

// --- State ---
const appointments = ref([]);
const loading = ref(false);
const currentPage = ref(1);
const totalPages = ref(1);
const totalRecords = ref(0);

const filterStatus = ref('All');
const searchQuery = ref('');

const todayDate = new Date().toISOString().split('T')[0];

const fetchAppointments = async () => {
  loading.value = true;
  try {
    const params = {
      page: currentPage.value,
      status: filterStatus.value !== 'All' ? filterStatus.value : undefined,
      search: searchQuery.value || undefined
    };
    const res = await getAppointments(params);
    appointments.value = res.data || [];
    if (res.pagination) {
      totalPages.value = res.pagination.total_pages || 1;
      totalRecords.value = res.pagination.total_items || 0;
    }
  } catch (error) {
    toast.error('Failed to load appointments. Please try again later.');
  } finally {
    loading.value = false;
  }
};

const pendingCount = computed(() => appointments.value.filter(a => a.status === 'Pending').length);

const isAptReady = (aptDate, aptTime) => {
  const appointmentDateTime = new Date(`${aptDate}T${aptTime}:00`);
  const now = new Date();

  const buffer = 5 * 60 * 1000;
  return now >= (appointmentDateTime - buffer);
};

// --- Pagination Helpers ---
const goToPage = (p) => {
  if (p >= 1 && p <= totalPages.value) {
    currentPage.value = p;
  }
};

const displayedPages = computed(() => {
  const current = currentPage.value;
  const last = totalPages.value;
  const delta = 2;
  const left = current - delta;
  const right = current + delta + 1;
  const range = [];
  const rangeWithDots = [];
  let l;

  for (let i = 1; i <= last; i++) {
    if (i === 1 || i === last || (i >= left && i < right)) {
      range.push(i);
    }
  }

  for (let i of range) {
    if (l) {
      if (i - l === 2) {
        rangeWithDots.push(l + 1);
      } else if (i - l !== 1) {
        rangeWithDots.push('...');
      }
    }
    rangeWithDots.push(i);
    l = i;
  }
  return rangeWithDots;
});

// --- Actions ---
const handleConfirm = async (id) => {
  try {
    await confirmAppointment(id);
    toast.success("Appointment confirmed successfully!");
    await fetchAppointments();
  } catch (error) {
    toast.error("Failed to confirm appointment.");
  }
};

const handleDecline = async (id) => {
  try {
    await cancelAppointment(id);
    toast.success("Appointment cancelled successfully!");
    await fetchAppointments();
  } catch (error) {
    toast.error("Failed to cancel appointment.");
  }
};

const now = ref(new Date());

watch(currentPage, fetchAppointments);

watch(searchQuery, () => {
  currentPage.value = 1;
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    getDocDetails();
  }, 500);
});

watch(filterStatus, () => {
  currentPage.value = 1;
  fetchAppointments();
});

onMounted(fetchAppointments);
onMounted(() => {
  const timer = setInterval(() => {
    now.value = new Date();
  }, 60000);

  return () => clearInterval(timer);
});


const getStatusClass = (status) => status?.toLowerCase() || 'pending';
</script>

<template>
  <div class="doctor-page-layout">
    <div class="schedule-container">
      <header class="schedule-header">
        <div class="header-content">
          <div class="title-group">
            <h1 class="page-title">Appointments Schedule</h1>
            <p class="page-subtitle">Manage your patient visits for the next 5 days</p>
          </div>
        </div>
      </header>

      <div class="filter-toolbar shadow-sm">
        <div class="filter-tabs">
          <button v-for="tab in ['All', 'Today', 'Pending', 'Confirmed']" :key="tab" @click="filterStatus = tab"
            :class="['tab-btn', { active: filterStatus === tab }]">
            {{ tab === 'Pending' ? 'Requests' : tab }}
            <span v-if="tab === 'Pending' && pendingCount > 0" class="badge-count">{{ pendingCount }}</span>
          </button>
        </div>

        <div class="search-box">
          <SearchIcon :size="18" class="search-icon" />
          <input v-model="searchQuery" type="text" placeholder="Search patient or ID..." />
        </div>
      </div>

      <div class="dashboard-card shadow-sm">
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <span>Syncing Schedule...</span>
        </div>

        <div class="table-view-container">
          <table class="modern-table">
            <thead>
              <tr class="table-header-row">
                <th>Appointment</th>
                <th>Patient Details</th>
                <th>Medical ID</th>
                <th>Specialty</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="apt in appointments" :key="apt._id" class="table-row">
                <td class="w-48">
                  <div class="time-container">
                    <span class="hour-text">{{ apt.time }}</span>
                    <span :class="['date-subtext', { 'text-blue-500 font-semibold': apt.date === todayDate }]">
                      {{ apt.date === todayDate ? 'Today' : apt.date }}
                    </span>
                  </div>
                </td>

                <td>
                  <div class="patient-profile-wrapper">
                    <div class="avatar-box">
                      {{apt.patient_name.split(' ').map(n => n[0]).join('').toUpperCase()}}
                    </div>
                    <div class="patient-meta">
                      <p class="p-fullname">{{ apt.patient_name }}</p>
                      <p class="p-demographics">{{ apt.patient_age }} years • {{ apt.patient_gender }}</p>
                    </div>
                  </div>
                </td>

                <td><code class="id-badge">{{ apt.medical_id }}</code></td>

                <td>
                  <div class="specialty-pill">
                    <StethoscopeIcon :size="14" class="icon-muted" />
                    <span>{{ apt.type }}</span>
                  </div>
                </td>

                <td>
                  <span :class="['status-indicator', getStatusClass(apt.status)]">
                    <span class="dot"></span>
                    {{ apt.status }}
                  </span>
                </td>

                <td class="text-right">
                  <div class="action-group">
                    <template v-if="apt.status === 'Pending'">
                      <button class="btn-confirm" @click="handleConfirm(apt._id)" title="Accept Request">
                        <CheckCircleIcon :size="18" />
                      </button>
                      <button class="btn-cancel" @click="handleDecline(apt._id)" title="Decline Request">
                        <XCircleIcon :size="18" />
                      </button>
                    </template>

                    <template v-else>
                      <button class="btn-icon" title="View History">
                        <HistoryIcon :size="18" />
                      </button>
                      <button class="btn-action-primary"
                        :title="!isAptReady(apt.date, apt.time) ? 'Session will be available at ' + apt.time : 'Start Session'"
                        @click="router.push(`/doctor/appointment/${apt._id}`)">
                        Start Session
                      </button>
                    </template>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>

          <nav v-if="totalPages > 1" class="pagination">
            <button class="page-link" :disabled="currentPage === 1" @click="goToPage(currentPage - 1)">
              &lsaquo;
            </button>

            <template v-for="(page, index) in displayedPages" :key="index">
              <span v-if="page === '...'" style="color: #cbd5e1; padding: 0 8px;">...</span>
              <button v-else :class="['page-link', { active: page === currentPage }]" @click="goToPage(page)">
                {{ page }}
              </button>
            </template>

            <button class="page-link" :disabled="currentPage === totalPages" @click="goToPage(currentPage + 1)">
              &rsaquo;
            </button>
          </nav>
        </div>
      </div>
    </div>
  </div>
</template>

<style src="../../styles/docAppointment.css" scoped></style>