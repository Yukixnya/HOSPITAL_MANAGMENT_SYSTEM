<script setup>
import { computed, onMounted, ref } from 'vue';
import {
  AlertTriangleIcon, DownloadIcon, CalendarIcon, HeartIcon, ActivityIcon,
  HistoryIcon, StethoscopeIcon, SyringeIcon, ScanIcon, PlusSquareIcon,
  ChevronRightIcon, DropletsIcon, UserIcon
} from 'lucide-vue-next';
import { useRoute } from "vue-router";
import { getPatientById } from '../../services/doctor';
import { useToast } from 'vue-toastification';

const toast = useToast();
const route = useRoute();
const loading = ref(true);
const medications = ref([]);
const timeline = ref([]);
const Patient = ref(null);

const id = computed(() => route.params.id || route.path.split("/").pop());

const getIconForType = (type) => {
  const icons = {
    checkup: StethoscopeIcon,
    vaccination: SyringeIcon,
    scan: ScanIcon,
  };
  return icons[type?.toLowerCase()] || ActivityIcon;
};

const getBgForType = (type) => {
  const bgs = {
    checkup: 'bg-blue-500',
    vaccination: 'bg-emerald-500',
    scan: 'bg-purple-500',
  };
  return bgs[type?.toLowerCase()] || 'bg-slate-500';
};

const getPatient = async () => {
  loading.value = true;
  try {
    const res = await getPatientById(id.value);
    Patient.value = res;
    medications.value = res.prescriptions || [];

    timeline.value = (res.recent_medical_records || []).map(record => ({
      date: new Date(record.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
      title: record.title,
      desc: record.description,
      icon: getIconForType(record.type),
      iconBg: getBgForType(record.type)
    }));
  } catch (error) {
    toast.error('Failed to fetch patient data. Please try again later.');
  } finally {
    loading.value = false;
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return 'No visits';
  return new Date(dateStr).toLocaleDateString(undefined, {
    year: 'numeric', month: 'short', day: 'numeric'
  });
}

onMounted(() => {
  getPatient();
});

const quickStats = computed(() => {
  if (!Patient.value) return [];
  return [
    { label: 'Last Visit', value: formatDate(Patient.value.last_visit), icon: CalendarIcon, color: 'text-blue-500', bg: 'bg-blue-50' },
    { label: 'Heart Rate', value: Patient.value.heart_rate || '--', icon: HeartIcon, color: 'text-rose-500', bg: 'bg-rose-50' },
    { label: 'Blood Pressure', value: Patient.value.blood_pressure || '--', icon: ActivityIcon, color: 'text-indigo-500', bg: 'bg-indigo-50' },
  ];
});
</script>

<template>
  <div class="patient-dashboard">
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p class="loading-text">Loading Patient Records...</p>
    </div>

    <div v-else-if="Patient" class="dashboard-content">
      <section class="card profile-card">
        <div class="profile-header-layout">
          <div class="profile-info-group">
            <div class="avatar-wrapper">
              <img :src="Patient.avatar || `https://ui-avatars.com/api/?name=${Patient.name}&background=random`"
                class="avatar-img" />
              <div class="avatar-badge">
                <UserIcon class="icon-xs" />
              </div>
            </div>
            
            <div class="profile-text">
              <div class="name-badge-row">
                <h1 class="patient-name">{{ Patient.name }}</h1>
                <span class="id-pill">ID: #{{ id.slice(-5) }}</span>
              </div>

              <div class="meta-data-row">
                <span class="meta-item"><CalendarIcon class="icon-xs" /> {{ Patient.age }} yrs</span>
                <span class="dot-separator"></span>
                <span class="meta-item">{{ Patient.gender }}</span>
                <span class="dot-separator"></span>
                <span class="meta-item blood-type">
                  <DropletsIcon class="icon-xs" /> <strong>{{ Patient.blood_type }}</strong>
                </span>
              </div>
            </div>
          </div>

          <div class="header-actions">
            <button class="btn btn-primary">
              <DownloadIcon class="icon-xs" /> Download EHR
            </button>
          </div>
        </div>

        <div class="stats-grid">
          <div v-for="stat in quickStats" :key="stat.label" class="stat-item-card">
            <div class="stat-item-header">
              <div :class="['stat-icon-box', stat.bg, stat.color]">
                <component :is="stat.icon" class="icon-md" />
              </div>
              <span class="stat-label-text">{{ stat.label }}</span>
            </div>
            <div class="stat-value-group">
              <span class="stat-value-number">{{ stat.value }}</span>
              <span v-if="stat.unit" class="stat-value-unit">{{ stat.unit }}</span>
            </div>
          </div>
        </div>
      </section>

      <div class="content-grid-layout">
        <main class="history-column">
          <div class="card timeline-container">
            <div class="section-title-bar">
              <h2 class="section-heading">
                <div class="icon-bg-blue">
                  <HistoryIcon class="icon-sm" />
                </div>
                Medical History Timeline
              </h2>
              <button class="text-link">
                View All <ChevronRightIcon class="icon-xs" />
              </button>
            </div>

            <div class="timeline-wrapper">
              <div v-for="event in timeline" :key="event.date" class="timeline-entry">
                <div :class="['timeline-marker', event.iconBg]">
                  <component :is="event.icon" class="icon-sm text-white" />
                </div>
                <div class="timeline-card">
                  <p class="entry-date">{{ event.date }}</p>
                  <h3 class="entry-title">{{ event.title }}</h3>
                  <p class="entry-description">{{ event.desc }}</p>
                </div>
              </div>
            </div>
          </div>
        </main>

        <aside class="meds-column">
          <div class="card meds-container">
            <div class="section-title-bar sticky-header">
              <h2 class="section-heading-sm">
                <div class="icon-bg-emerald">
                  <PlusSquareIcon class="icon-sm" />
                </div>
                Active Medications
              </h2>
              <span class="count-pill">{{ medications.length }}</span>
            </div>

            <div class="med-list-gap">
              <div v-for="med in medications" :key="med.name" class="med-item-card">
                <div class="med-item-top">
                  <div class="med-identity">
                    <h3 class="med-title-text">{{ med.name }}</h3>
                    <div class="med-tag-row">
                      <span class="tag-blue">{{ med.dosage }}</span>
                      <span class="tag-slate">{{ med.duration }}</span>
                    </div>
                  </div>
                  <span :class="['freq-pill', med.frequency === 'As needed' ? 'pill-amber' : 'pill-emerald']">
                    {{ med.frequency }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </div>

    <div v-else class="error-view">
      <div class="error-card">
        <AlertTriangleIcon class="error-icon-lg" />
        <h2 class="error-title">Patient Not Found</h2>
        <p class="error-message">The record you are looking for does not exist or has been moved.</p>
        <button @click="$router.back()" class="btn-retry">Go Back</button>
      </div>
    </div>
  </div>
</template>

<style src="../../styles/docPatientProf.css" scoped></style>