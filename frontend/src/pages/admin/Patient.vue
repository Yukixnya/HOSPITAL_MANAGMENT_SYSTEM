<script setup>
import { ref, onMounted, watch } from 'vue';
import {
  Search, SlidersHorizontal, ChevronLeft, ChevronRight,
  Calendar as CalendarIcon, ChevronDown
} from 'lucide-vue-next';
import { getPatients } from '../../services/admin';

// Filter States
const searchQuery = ref('');

//state managment
const patients = ref([])
const currentPage = ref(1)
const totalPages = ref(1)
const totalRecords = ref(0)
let searchTimeout = null

// fetch patient data
const getAllPatients = async () => {
  try {
    const params = {
      page: currentPage.value,
      search: searchQuery.value.trim() || undefined
    }

    console.log("params", params)

    const res = await getPatients(params);
    totalRecords.value = res.total
    totalPages.value = res.total_pages
    patients.value = res.data
  } catch (error) {
    alert(error.message)
  }
}

// debouncing search
watch(searchQuery, () => {
  currentPage.value = 1 // Reset to page 1 on filter change
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    fetchDoctorList()
  }, 400)
})

watch([currentPage, searchQuery], () => getAllPatients())

onMounted(() => getAllPatients())

// --- Pagination ---
const nextPage = () => { if (currentPage.value < totalPages.value) currentPage.value++ }
const prevPage = () => { if (currentPage.value > 1) currentPage.value-- }

//search Patient
// const searchPatient = async () => {
//   try {

//   } catch (error) {
//     alert(error.message)
//   }
// }

const getConditionClass = (condition) => {
  switch (condition) {
    case 'Stable': return 'bg-emerald-50 text-emerald-600';
    case 'Critical': return 'bg-red-50 text-red-600';
    case 'Observing': return 'bg-amber-50 text-amber-600';
    case 'Discharged': return 'bg-slate-100 text-slate-500';
    default: return 'bg-blue-50 text-blue-600';
  }
};
</script>

<template>
  <div class="p-8 bg-slate-50 min-h-screen font-sans">

    <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm mb-8 flex flex-wrap items-end gap-6">
      <div class="flex-1 min-w-75 space-y-1.5">
        <label class="text-[10px] font-bold text-slate-400 uppercase tracking-wider ml-1">Search Patients</label>
        <div class="relative">
          <Search class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" :size="18" />
          <input v-model.trim="searchQuery" type="text" placeholder="Search by name, ID, or phone..."
            class="w-full pl-10 pr-4 h-11 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all" />
        </div>
      </div>
    </div>

    <div class="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="text-[11px] font-bold text-slate-400 uppercase tracking-widest border-b border-slate-50">
              <th class="px-6 py-5">Patient Name</th>
              <th class="px-6 py-5">Medical ID</th>
              <th class="px-6 py-5">Age/Gender</th>
              <th class="px-6 py-5">Admission Date</th>
              <th class="px-6 py-5">Last Visit</th>
              <th class="px-6 py-5 text-center">Condition</th>
              <!-- <th class="px-6 py-5 text-right">Actions</th> -->
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-50">
            <tr v-for="patient in patients" :key="patient.id" class="hover:bg-slate-50/50 transition-colors group">
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div
                    class="h-10 w-10 rounded-full bg-blue-50 flex items-center justify-center text-blue-600 font-bold text-xs">
                    {{patient.name.split(' ').map(n => n[0]).join('')}}
                  </div>
                  <div>
                    <p class="font-bold text-slate-800 text-sm leading-tight">{{ patient.name }}</p>
                    <p class="text-[11px] text-slate-400 font-medium mt-0.5">{{ patient.mobile }}</p>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4">
                <span class="text-sm font-medium text-slate-600 bg-slate-50 px-2 py-1 rounded-md">{{ patient.medical_id
                }}</span>
              </td>
              <td class="px-6 py-4">
                <span class="text-sm text-slate-600 font-medium">{{ patient.age }} / {{ patient.gender }}</span>
              </td>
              <td class="px-6 py-4 text-sm text-slate-500">{{ patient.admission_date }}</td>
              <td class="px-6 py-4 text-sm text-slate-500">{{ patient.last_visit }}</td>
              <td class="px-6 py-4 text-center">
                <span
                  :class="[getConditionClass(patient.condition), 'text-[10px] font-bold px-3 py-1 rounded-full uppercase tracking-tight inline-block min-w-20 text-center shadow-sm border border-current/5']">
                  {{ patient.condition }}
                </span>
              </td>
              <!-- <td class="px-6 py-4 text-right">
                <button class="text-blue-600 text-sm font-bold hover:text-blue-700 hover:underline transition-all">
                  View Profile
                </button>
              </td> -->
            </tr>
          </tbody>
        </table>
      </div>

      <div class="px-6 py-4 border-t border-slate-100 flex items-center justify-between bg-white">
        <div class="text-sm text-slate-500">
          Showing <span class="font-bold text-slate-800">{{ ((currentPage - 1) * 10) + 1 }} to {{ Math.min(currentPage *
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
  </div>
</template>

<style scoped>
/* Remove default date icon to use Lucide component instead */
input[type="date"]::-webkit-calendar-picker-indicator {
  opacity: 0;
  cursor: pointer;
}
</style>