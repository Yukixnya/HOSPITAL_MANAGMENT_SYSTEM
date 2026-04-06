<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import {
  Search, ChevronLeft, ChevronRight, Loader2
} from 'lucide-vue-next';
import { getPatients } from '../../services/admin';
import { useToast } from 'vue-toastification';

const toast = useToast();

// --- State Management ---
const patients = ref([]);
const currentPage = ref(1);
const totalPages = ref(1);
const totalRecords = ref(0);
const searchQuery = ref('');
const isLoading = ref(false);
let searchTimeout = null;

// --- Fetch Data ---
const getAllPatients = async () => {
  isLoading.value = true;
  try {
    const params = {
      page: currentPage.value,
      search: searchQuery.value.trim() || undefined
    };
    const res = await getPatients(params);
    patients.value = res.data || [];
    totalRecords.value = res.total || 0;
    totalPages.value = res.total_pages || 1;
  } catch (error) {
    toast.error("Failed to load patients. Please try again.");
  } finally {
    isLoading.value = false;
  }
};

// --- Watchers ---
watch(searchQuery, () => {
  currentPage.value = 1;
  if (searchTimeout) clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => getAllPatients(), 400);
});

watch(currentPage, () => getAllPatients());
onMounted(() => getAllPatients());

// --- Pagination ---
const nextPage = () => { if (currentPage.value < totalPages.value) currentPage.value++ };
const prevPage = () => { if (currentPage.value > 1) currentPage.value-- };

const pages = computed(() => {
  const arr = [];
  for (let i = 1; i <= Math.min(totalPages.value, 5); i++) arr.push(i);
  return arr;
});

const getConditionClass = (condition) => {
  switch (condition?.toLowerCase()) {
    case 'stable': return 'is-stable';
    case 'critical': return 'is-critical';
    case 'observing': return 'is-observing';
    case 'discharged': return 'is-discharged';
    default: return 'is-default';
  }
};
</script>

<template>
  <div class="main-wrapper">
    <div class="content-container">
      
      <header class="page-header">
        <div class="filters-left">
          <div class="filter-group search-group">
            <label class="label-text">Search Patients</label>
            <div class="relative-input">
              <Search class="input-icon-left" :size="18" />
              <input v-model.trim="searchQuery" type="text" placeholder="Search by name, ID, or phone..." class="styled-input" />
            </div>
          </div>
        </div>
      </header>

      <div class="table-card">
        <div v-if="isLoading" class="loader-overlay">
          <Loader2 class="spinner" :size="32" />
          <span class="loader-text">Fetching Records...</span>
        </div>

        <div class="table-scroll">
          <table class="data-table">
            <thead>
              <tr>
                <th>Patient Name</th>
                <th>Medical ID</th>
                <th>Age/Gender</th>
                <th>Admission</th>
                <th>Last Visit</th>
                <th class="text-center">Condition</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="patient in patients" :key="patient.id">
                <td>
                  <div class="doc-info-flex">
                    <div class="avatar-circle">
                      {{ patient.name.split(' ').map(n => n[0]).join('') }}
                    </div>
                    <div>
                      <p class="doc-name-text">{{ patient.name }}</p>
                      <p class="doc-email-text">{{ patient.mobile }}</p>
                    </div>
                  </div>
                </td>
                <td>
                  <span class="id-badge">{{ patient.medical_id }}</span>
                </td>
                <td>
                  <span class="text-medium">{{ patient.age }} / {{ patient.gender }}</span>
                </td>
                <td><span class="text-muted">{{ patient.admission_date }}</span></td>
                <td><span class="text-muted">{{ patient.last_visit }}</span></td>
                <td class="text-center">
                  <span :class="['status-pill', getConditionClass(patient.condition)]">
                    <span class="dot"></span>
                    {{ patient.condition?.toUpperCase() }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <footer class="table-footer">
          <p class="footer-count">Showing <b>{{ ((currentPage - 1) * 10) + 1 }} - {{ Math.min(currentPage * 10, totalRecords) }}</b> of {{ totalRecords }}</p>
          <div class="pagination-controls">
            <button @click="prevPage" :disabled="currentPage === 1" class="page-arrow"><ChevronLeft :size="18"/></button>
            <div class="page-list">
              <button v-for="p in pages" :key="p" @click="currentPage = p" :class="['page-num', {active: currentPage === p}]">{{ p }}</button>
            </div>
            <button @click="nextPage" :disabled="currentPage >= totalPages" class="page-arrow"><ChevronRight :size="18"/></button>
          </div>
        </footer>
      </div>

    </div>
  </div>
</template>

<style src="../../styles/adminDoctor.css" scoped></style>