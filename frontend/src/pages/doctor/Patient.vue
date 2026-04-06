<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { 
    SearchIcon, FilterIcon, DownloadIcon, EyeIcon, 
    MoreVerticalIcon, ChevronLeftIcon, ChevronRightIcon 
} from 'lucide-vue-next';
import { getPatients } from '../../services/doctor';
import { useToast } from 'vue-toastification';

const toast = useToast();
const patients = ref([]);
const currentPage = ref(1);
const totalPages = ref(1);
const totalRecords = ref(0);
const searchQuery = ref(''); 
const patientFilter = ref('All Patients');
const isLoading = ref(false);

let searchTimeout = null;

const getPatientsDetails = async () => {
    isLoading.value = true;
    try {
        const params = {
            page: currentPage.value,
            filter: patientFilter.value === 'All Patients' ? undefined : patientFilter.value,
            search: searchQuery.value || undefined
        };
        
        const res = await getPatients(params);

        patients.value = res.data;
        totalPages.value = res.pagination?.total_pages || 1;
        totalRecords.value = res.pagination?.total_items || 0;
    } catch (error) {
        toast.error('Failed to fetch patient data. Please try again later.');
    } finally {
        isLoading.value = false;
    }
};

// --- Watchers ---

watch(searchQuery, () => {
    currentPage.value = 1;
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        getPatientsDetails();
    }, 500);
});

// Watch Filter Dropdown
watch(patientFilter, () => {
    currentPage.value = 1;
    getPatientsDetails();
});

// Watch Pagination
watch(currentPage, () => {
    getPatientsDetails();
});

onMounted(() => {
    getPatientsDetails();
});

// --- Helpers ---
const nextPage = () => { if (currentPage.value < totalPages.value) currentPage.value++ };
const prevPage = () => { if (currentPage.value > 1) currentPage.value-- };

const pages = computed(() => {
  const arr = [];
  for (let i = 1; i <= Math.min(totalPages.value, 5); i++) arr.push(i);
  return arr;
});

const getInitials = (name) => name ? name.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase() : '??';

const formatDate = (dateStr) => {
    if (!dateStr) return { day: 'N/A', year: '' };
    const date = new Date(dateStr);
    return {
        day: date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
        year: date.getFullYear()
    };
};

const conditionStyles = (cond) => {
    const map = {
        'Observing': 'bg-blue-50',
        'Critical': 'bg-red-50',
        'Healthy': 'bg-green-50',
        'Recovering': 'bg-purple-50',
        'Under Treatment': 'bg-orange-50',
        'Discharged': 'bg-gray-100',
    };
    return map[cond] || 'bg-gray-50';
};

const exportToCSV = () => {
    if (!patients.value.length) return;

    const headers = [
        "Name",
        "Medical ID",
        "Gender",
        "Age",
        "Mobile",
        "Email",
        "Condition",
        "Last Visit",
        "Admission Date"
    ];

    const rows = patients.value.map(p => [
        p.name,
        p.medical_id,
        p.gender,
        p.age,
        p.mobile,
        p.email,
        p.condition,
        p.last_visit,
        p.admission_date
    ]);

    const csvContent = [
        headers.join(","), 
        ...rows.map(row => row.map(val => `"${val ?? ''}"`).join(","))
    ].join("\n");

    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.setAttribute("download", `patients_${new Date().toISOString().split("T")[0]}.csv`);

    document.body.appendChild(link);
    link.click();

    document.body.removeChild(link);
};
</script>

<template>
    <div class="patients-container">
        <div class="dashboard-controls">
            <div class="search-container">
                <SearchIcon class="search-icon" :size="18" />
                <input v-model.trim="searchQuery" type="text" placeholder="Search patients by name, ID, or phone..."
                    class="search-input" />
            </div>

            <div class="filter-actions">
                <div class="select-wrapper">
                    <FilterIcon class="select-icon" :size="14" />
                    <select v-model="patientFilter"  class="status-select">
                        <option
                            v-for="tab in ['All Patients', 'Observing', 'Healthy', 'Critical', 'Recovering', 'Under Treatment', 'Discharged']"
                            :key="tab" :value="tab">
                            {{ tab }}
                        </option>
                    </select>
                </div>

                <button class="action-btn export-btn" @click="exportToCSV">
                    <DownloadIcon :size="16" />
                    <span>Export</span>
                </button>
            </div>
        </div>

        <div class="table-card">
            <div style="overflow-x: auto;">
                <table class="patient-table">
                    <thead>
                        <tr>
                            <th>Patient Details</th>
                            <th>Contact</th>
                            <th>Last Visit</th>
                            <th>Condition</th>
                            <th>Admission</th>
                            <th style="text-align: right;">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="patient in patients" :key="patient._id">
                            <td>
                                <div class="patient-identity">
                                    <div class="avatar-circle">{{ getInitials(patient.name) }}</div>
                                    <div>
                                        <div class="patient-name">{{ patient.name }}</div>
                                        <div class="patient-sub">{{ patient.medical_id }} • {{ patient.gender }}, {{
                                            patient.age }}</div>
                                    </div>
                                </div>
                            </td>
                            <td>
                                <div style="font-size: 14px;">{{ patient.mobile }}</div>
                                <div style="font-size: 10px; color: #94a3b8;">{{ patient.email }}</div>
                            </td>
                            <td>
                                <div style="font-size: 14px; font-weight: 500;">{{ formatDate(patient.last_visit).day }}
                                </div>
                                <div style="font-size: 10px; color: #94a3b8; font-weight: 700;">{{
                                    formatDate(patient.last_visit).year }}</div>
                            </td>
                            <td>
                                <span class="badge" :class="conditionStyles(patient.condition)">
                                    {{ patient.condition }}
                                </span>
                            </td>
                            <td style="font-size: 14px; color: #64748b;">{{ patient.admission_date }}</td>
                            <td style="text-align: right;">
                                <router-link :to="`/doctor/patients/${patient._id}`"
                                    style="color: #2563eb; margin-right: 10px;">
                                    <EyeIcon :size="20" />
                                </router-link>
                                <button style="background: none; border: none; color: #cbd5e1; cursor: pointer;">
                                    <MoreVerticalIcon :size="20" />
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <footer class="table-footer">
                <p style="font-size: 13px; color: #64748b;">
                    Showing <b>{{ ((currentPage - 1) * 10) + 1 }} - {{ Math.min(currentPage * 10, totalRecords) }}</b>
                    of {{ totalRecords }}
                </p>
                <div class="pagination-controls">
                    <button @click="prevPage" :disabled="currentPage === 1" class="page-num">
                        <ChevronLeftIcon :size="16" />
                    </button>
                    <button v-for="p in pages" :key="p" @click="currentPage = p"
                        :class="['page-num', { active: currentPage === p }]">
                        {{ p }}
                    </button>
                    <button @click="nextPage" :disabled="currentPage >= totalPages" class="page-num">
                        <ChevronRightIcon :size="16" />
                    </button>
                </div>
            </footer>
        </div>
    </div>
</template>

<style src="../../styles/doctorPatient.css" scoped></style>