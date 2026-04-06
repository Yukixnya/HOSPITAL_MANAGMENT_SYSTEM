<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { medHistory } from '../../services/patient';
import { useToast } from 'vue-toastification';

const toast = useToast();
const router = useRouter();

const historyStats = ref([]);
const medicalRecords = ref([]);
const isLoading = ref(true); 
const isFetchingMore = ref(false); 

const currentPage = ref(1);
const hasNextPage = ref(false);

const getRecordUI = (type) => {
  const map = {
    'Checkup Report': { icon: '📋', tagClass: 'bg-blue-50 text-blue-600', markerClass: 'text-blue-500', actionLabel: 'Report' },
    'Lab Test': { icon: '🔬', tagClass: 'bg-green-50 text-green-600', markerClass: 'text-green-500', actionLabel: 'Results' },
    'Vaccination': { icon: '💉', tagClass: 'bg-purple-50 text-purple-600', markerClass: 'text-purple-500', actionLabel: 'Cert' }
  };
  return map[type] || { icon: '📄', tagClass: 'bg-slate-50 text-slate-600', markerClass: 'text-slate-400', actionLabel: 'View' };
};

const fetchHistory = async (page = 1) => {
  try {
    if (page === 1) isLoading.value = true;
    else isFetchingMore.value = true;

    const res = await medHistory({ page });

    if (page === 1) historyStats.value = res.historyStats || [];
    
    hasNextPage.value = res.pagination?.has_next || false;
    currentPage.value = res.pagination?.current_page || 1;

    const newRecords = (res.medicalRecords || []).map(record => {
      const dateObj = new Date(record.date);
      const ui = getRecordUI(record.type);
      return {
        ...record,
        ...ui,
        year: dateObj.getFullYear(),
        formattedDate: dateObj.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
        time: dateObj.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
        status: record.status || 'Ready' 
      };
    });

    medicalRecords.value = [...medicalRecords.value, ...newRecords];

  } catch (error) {
    toast.error("Failed to fetch medical history.");
  } finally {
    isLoading.value = false;
    isFetchingMore.value = false;
  }
};

const loadMore = () => {
  if (hasNextPage.value && !isFetchingMore.value) {
    fetchHistory(currentPage.value + 1);
  }
};

onMounted(() => {
  fetchHistory(1);
});
</script>

<template>
  <div v-if="isLoading" style="display: flex; align-items: center; justify-content: center; min-height: 100vh;">
    <div class="animate-spin" style="width: 48px; height: 48px; border: 3px solid #e2e8f0; border-top-color: #2563eb; border-radius: 50%;"></div>
  </div>

  <div v-else class="history-page">
    <header style="margin-bottom: 40px;">
      <h1 class="text-3xl">Complete Medical History</h1>
      <p style="color: #64748b; font-weight: 500; margin-top: 8px;">A chronological overview of your health journey.</p>
    </header>

    <section class="stats-grid">
      <div v-for="stat in historyStats" :key="stat.label" class="stat-card">
        <div :class="['stat-icon-box', stat.bgClass]" 
             style="width: 48px; height: 48px; border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 20px;">
          {{ stat.icon }}
        </div>
        <div>
          <p class="label-caps" style="color: #94a3b8; margin: 0;">{{ stat.label }}</p>
          <p class="text-2xl">{{ stat.value }}</p>
        </div>
      </div>
    </section>

    <div class="timeline-container">
      
      <div v-for="(item, index) in medicalRecords" :key="item.id" class="record-item">
        
        <div v-if="index === 0 || item.year !== medicalRecords[index-1].year" class="year-tag">
          {{ item.year }}
        </div>

        <div class="timeline-icon">
          {{ item.icon }}
        </div>

        <div class="record-card">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; flex-wrap: wrap; gap: 16px;">
            <div style="display: flex; align-items: center; gap: 12px;">
              <span :class="['label-caps', item.tagClass]" style="padding: 4px 10px; border-radius: 8px; background: #f1f5f9;">
                {{ item.type }}
              </span>
              <span style="font-size: 12px; font-weight: 700; color: #94a3b8;">{{ item.formattedDate }}</span>
            </div>
            
            <div style="display: flex; gap: 8px;">
              <button class="btn-secondary-sm">📄 {{ item.actionLabel }}</button>
              <button @click="router.push(`/patient/record/${item.id}`)" class="btn-primary-sm">
                View Report
              </button>
            </div>
          </div>

          <h3 style="font-size: 20px; font-weight: 900; margin: 0 0 8px 0;">{{ item.title }}</h3>
          <p style="font-size: 14px; color: #64748b; line-height: 1.6; margin-bottom: 24px;">{{ item.description }}</p>

          <div style="display: flex; gap: 24px; padding-top: 24px; border-top: 1px solid #f8fafc;">
            <div style="display: flex; align-items: center; gap: 8px;">
              <span class="label-caps" style="color: #cbd5e1;">Provider:</span>
              <span style="font-size: 12px; font-weight: 700; color: #1e293b;">{{ item.provider }}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
              <span class="label-caps" style="color: #cbd5e1;">Status:</span>
              <span :style="{ color: item.status === 'Ready' ? '#22c55e' : '#f97316' }" style="font-size: 12px; font-weight: 700;">
                ● {{ item.status }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div v-if="hasNextPage" style="padding-top: 16px;">
        <button @click="loadMore" 
                style="width: 100%; padding: 16px; border: 2px solid #f1f5f9; background: transparent; border-radius: 20px; font-weight: 900; color: #94a3b8; cursor: pointer; transition: 0.2s;">
          View Older Records
        </button>
      </div>

    </div>
  </div>
</template>

<style src="./styles/medHistory.css" scoped></style>