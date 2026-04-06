<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { getDoctors } from '../../services/patient';
import { useToast } from 'vue-toastification';

const toast = useToast();
const router = useRouter();
const doctors = ref([]);
const currentPage = ref(1);
const totalPages = ref(1);
const totalRecords = ref(0);
const searchQuery = ref('');
let searchTimeout = null;

const getDocDetails = async () => {
  try {
    const params = {
      page: currentPage.value,
      search: searchQuery.value || undefined
    };
    const res = await getDoctors(params);
    doctors.value = res.data || [];
    totalPages.value = res.pagination?.total_pages || 1;
    totalRecords.value = res.pagination?.total_items || 0;
  } catch (error) {
    toast.error('Failed to fetch doctor details.');
  }
};

watch(searchQuery, () => {
  currentPage.value = 1;
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    getDocDetails();
  }, 500);
});

// Watch Page Changes
watch(currentPage, () => {
  getDocDetails();
});

onMounted(() => {
  getDocDetails();
});

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
</script>

<template>
  <div class="specialist-page">
    <header class="header-flex">
      <div>
        <h1 class="text-3xl">Find a Healthcare Specialist</h1>
        <p class="text-slate-500">
          Discover and book appointments with {{ totalRecords }} certified professionals.
        </p>
      </div>

      <div class="search-input-wrapper">
        <span class="search-icon">🔍</span>
        <input v-model="searchQuery" type="text" placeholder="Search by name, clinic..." class="search-input">
      </div>
    </header>

    <span class="label-caps">Showing Page {{ currentPage }} of {{ totalPages }}</span>

    <main v-if="doctors.length">
      <div v-for="doc in doctors" :key="doc.id" class="doctor-card" @click="router.push(`/patient/doctors/${doc.id}`)">
        <div class="profile-info">
          <div class="doc-avatar">
            <img v-if="doc.image" :src="doc.image" class="doc-avatar-img" />
            <span v-else>{{ doc.name.charAt(0) }}{{ doc.name.split(' ')[1]?.charAt(0) }}</span>

            <div :class="['online-dot', doc.online ? 'bg-green' : 'bg-grey']"></div>
          </div>
          <div>
            <h3 class="doc-name">{{ doc.name }}</h3>
            <span class="specialty-tag">{{ doc.specialty }}</span>
            <span class="rating">★ {{ doc.rating || '5.0' }}</span>
          </div>
        </div>

        <div class="column-section">
          <p class="column-label">Location</p>
          <p class="column-text">{{ doc.clinic || 'N/A' }}</p>
        </div>

        <div class="bio-container" style="flex: 1;">
          <p class="bio-text">{{ doc.bio }}</p>
        </div>

        <div class="fee-section">
          <p class="column-label">Fee</p>
          <p class="fee-amount">${{ doc.fee }}</p>
        </div>

        <button class="btn-book" @click.stop="router.push(`/patient/doctors/${doc.id}`)">
          Book Now
        </button>
      </div>
    </main>

    <main v-else class="text-slate-500" style="padding: 40px; text-align: center;">
      No specialists found matching your search.
    </main>

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
</template>

<style src="./styles/docList.css" scoped></style>
