<script setup>
import { onMounted, ref, watch, computed } from 'vue'
import {
  ChevronLeft, ChevronRight, Edit2, Trash2,
  UserCheck, UserPlus, ClipboardList, ChevronDown,
  Search, Download, Check, X, Loader2
} from 'lucide-vue-next'

import DialogueBox from '../../components/DialogueBox.vue'
import { filterDoctors, updateDoc, updateDocStatus, getDoctors } from '../../services/admin'
import { specializations } from '../../utils/DoctorSpecialization'
import { schedules } from "../../utils/DoctorSchedule"

// --- State Management ---
const doctors = ref([])
const currentPage = ref(1)
const totalPages = ref(1)
const totalRecords = ref(0)
const searchQuery = ref("")
const isLoading = ref(false)
let searchTimeout = null

// Filters
const selectedDepartment = ref('All Departments')
const selectedStatus = ref('All Status')

// Edit Mode State
const editingId = ref(null)
const editForm = ref({})

// --- Data Fetching ---
const fetchDoctorList = async () => {
  isLoading.value = true
  try {
    const params = {
      page: currentPage.value,
      search: searchQuery.value.trim() || undefined,
      status: selectedStatus.value !== "All Status" ? selectedStatus.value : undefined,
      specialization: selectedDepartment.value !== "All Departments" ? selectedDepartment.value : undefined
    }

    let res;
    const isSearching = params.search || params.status || params.specialization;

    if (isSearching) {
      res = await filterDoctors(params);
    } else {
      res = await getDoctors(currentPage.value);
    }

    console.log("value from search", res)
    doctors.value = res.data
    totalPages.value = res.total_pages
    totalRecords.value = res.total
  } catch (error) {
    console.error("Error fetching doctors:", error.message)
  } finally {
    isLoading.value = false
  }
}

// --- Watchers ---
// Debounced Search & Filter Watcher
watch([searchQuery, selectedDepartment, selectedStatus], () => {
  currentPage.value = 1 // Reset to page 1 on filter change
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    fetchDoctorList()
  }, 400)
})

// Immediate Page Watcher
watch(currentPage, () => {
  fetchDoctorList()
})

onMounted(() => fetchDoctorList())

// --- Inline Edit Actions ---
const startEdit = (doc) => {
  editingId.value = doc._id
  editForm.value = { ...doc, name: doc.user?.name || doc.name }
}

const cancelEdit = () => {
  editingId.value = null
  editForm.value = {}
}

const saveEdit = async () => {
  try {
    await updateDoc(editingId.value, editForm.value)
    await fetchDoctorList()
    cancelEdit()
  } catch (error) {
    alert("Failed to save: " + error.message)
  }
}

const updateStatus = async (doc, newStatus) => {
  try {
    await updateDocStatus(doc._id, newStatus)
    doc.status = newStatus // Optimistic Update
  } catch (error) {
    alert(error.message)
  }
}

const deactiveAcc = ref(null)
const deactive = async (name) => {
  const ok = await deactiveAcc.value.open(`Are you sure you wanted to deactivate Dr. ${name}?`)
  if (ok) {
    // Call delete/deactivate API here
    alert("Doctor has been deactivated")
  }
}

// --- Pagination Helpers ---
const nextPage = () => { if (currentPage.value < totalPages.value) currentPage.value++ }
const prevPage = () => { if (currentPage.value > 1) currentPage.value-- }
const pages = computed(() => {
  const range = 1
  let start = Math.max(1, currentPage.value - range)
  let end = Math.min(totalPages.value, currentPage.value + range)

  if (currentPage.value <= range) {
    end = Math.min(totalPages.value, 1 + range * 2)
  }

  if (currentPage.value + range >= totalPages.value) {
    start = Math.max(1, totalPages.value - range * 2)
  }

  const arr = []
  for (let i = start; i <= end; i++) {
    arr.push(i)
  }

  return arr
})

const getStatusStyle = (status) => {
  switch (status) {
    case 'Active': return 'bg-emerald-50 text-emerald-600'
    case 'On Leave': return 'bg-orange-50 text-orange-600'
    case 'Inactive': return 'bg-slate-100 text-slate-500'
    default: return 'bg-gray-50 text-gray-600'
  }
}

const stats = computed(() => [
  { title: 'TOTAL REGISTERED', value: totalRecords.value, icon: UserCheck, color: 'text-blue-600', bg: 'bg-blue-50' },
  { title: 'ON DUTY NOW', value: '42', icon: UserPlus, color: 'text-emerald-600', bg: 'bg-emerald-50' },
  { title: 'PENDING PROFILES', value: '3', icon: ClipboardList, color: 'text-orange-600', bg: 'bg-orange-50' },
])
</script>

<template>
  <div class="p-6 bg-slate-50 min-h-screen">
    <div class="flex flex-col lg:flex-row lg:items-end justify-between gap-6 mb-6 mx-10">
      <div class="flex flex-wrap items-center gap-4 flex-1">
        <div class="flex flex-col gap-1.5 flex-1 min-w-75">
          <label class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Search Doctor</label>
          <div class="relative">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" :size="18" />
            <input v-model.trim="searchQuery" type="text" placeholder="Search by name or specialization..."
              class="w-full bg-white border border-slate-200 rounded-xl pl-10 pr-4 py-2.5 text-sm font-medium text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all shadow-sm" />
          </div>
        </div>

        <div class="flex flex-col gap-1.5">
          <label class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Department</label>
          <div class="relative min-w-48">
            <select v-model="selectedDepartment"
              class="w-full appearance-none bg-white border border-slate-200 rounded-xl px-4 py-2.5 text-sm font-medium text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500/20 cursor-pointer shadow-sm">
              <option>All Departments</option>
              <option v-for="s in specializations" :key="s" :value="s">{{ s }}</option>
            </select>
            <ChevronDown class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none"
              :size="18" />
          </div>
        </div>

        <div class="flex flex-col gap-1.5">
          <label class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Status</label>
          <div class="relative min-w-40">
            <select v-model="selectedStatus"
              class="w-full appearance-none bg-white border border-slate-200 rounded-xl px-4 py-2.5 text-sm font-medium text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500/20 cursor-pointer shadow-sm">
              <option>All Status</option>
              <option value="Active">Active</option>
              <option value="On Leave">On Leave</option>
              <option value="Inactive">Inactive</option>
            </select>
            <ChevronDown class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none"
              :size="18" />
          </div>
        </div>
      </div>

      <button
        class="flex items-center gap-2 px-4 py-2.5 bg-white border border-slate-200 rounded-xl text-sm font-bold text-slate-700 hover:bg-slate-50 shadow-sm transition-all">
        <Download :size="18" class="text-slate-400" /> Export
      </button>
    </div>

    <div class="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden mb-8 mx-10 relative">
      <div v-if="isLoading"
        class="absolute inset-0 bg-white/60 backdrop-blur-[1px] z-10 flex items-center justify-center">
        <div class="flex flex-col items-center gap-2">
          <Loader2 class="animate-spin text-blue-600" :size="32" />
          <span class="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Syncing Data...</span>
        </div>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="text-[11px] font-bold text-slate-400 uppercase border-b bg-slate-50/50">
              <th class="px-6 py-4">Doctor Name</th>
              <th class="px-6 py-4">Specialization</th>
              <th class="px-6 py-4">Schedule</th>
              <th class="px-6 py-4">Experience</th>
              <th class="px-6 py-4">Status</th>
              <th class="px-6 py-4 text-right">Actions</th>
            </tr>
          </thead>

          <tbody class="divide-y divide-slate-50">
            <tr v-for="doc in doctors" :key="doc._id"
              :class="[editingId === doc._id ? 'bg-blue-50/40' : 'hover:bg-slate-50/80', 'transition-colors']">

              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div
                    class="h-10 w-10 rounded-full bg-blue-50 flex items-center justify-center text-blue-600 font-bold text-xs uppercase">
                    {{(doc.name || '??').split(' ').map(n => n[0]).join('')}}
                  </div>
                  <div>
                    <input v-if="editingId === doc._id" v-model="editForm.name"
                      class="border border-blue-200 rounded px-2 py-1 text-sm outline-none" />
                    <p v-else class="font-bold text-sm text-slate-800">{{ doc.name }}</p>
                    <p class="text-[10px] text-slate-400 font-medium tracking-tight">{{ doc.user?.email }}</p>
                  </div>
                </div>
              </td>

              <td class="px-6 py-4">
                <select v-if="editingId === doc._id" v-model="editForm.specialization"
                  class="border border-blue-200 rounded px-2 py-1 text-sm">
                  <option v-for="s in specializations" :key="s" :value="s">{{ s }}</option>
                </select>
                <p v-else class="text-sm font-medium text-slate-700">{{ doc.specialization }}</p>
              </td>

              <td class="px-6 py-4">
                <select v-if="editingId === doc._id" v-model="editForm.schedule"
                  class="border border-blue-200 rounded px-2 py-1 text-sm">
                  <option v-for="s in schedules" :key="s" :value="s">{{ s }}</option>
                </select>
                <p v-else class="text-sm text-slate-500">{{ doc.schedule }}</p>
              </td>

              <td class="px-6 py-4">
                <input v-if="editingId === doc._id" type="number" v-model="editForm.experience"
                  class="w-16 border border-blue-200 rounded px-2 py-1 text-sm" />
                <p v-else class="text-sm text-slate-700 font-semibold">{{ doc.experience }} Yrs</p>
              </td>

              <td class="px-6 py-4">
                <div class="relative w-fit group">
                  <span
                    :class="['px-3 py-1 rounded-full text-[10px] font-bold flex items-center gap-1.5 transition-all group-hover:ring-2 group-hover:ring-slate-200', getStatusStyle(doc.status)]">
                    <span class="h-1.5 w-1.5 rounded-full bg-current animate-pulse"></span>
                    {{ doc.status.toUpperCase() }}
                    <ChevronDown :size="10" class="ml-0.5 opacity-50" />
                  </span>
                  <select @change="updateStatus(doc, $event.target.value)"
                    class="absolute inset-0 w-full h-full opacity-0 cursor-pointer appearance-none">
                    <option value="Active">Active</option>
                    <option value="On Leave">On Leave</option>
                    <option value="Inactive">Inactive</option>
                  </select>
                </div>
              </td>

              <td class="px-6 py-4 text-right">
                <div v-if="editingId === doc._id" class="flex justify-end gap-3 text-emerald-600">
                  <button @click="saveEdit" class="hover:scale-120 transition-transform">
                    <Check :size="20" />
                  </button>
                  <button @click="cancelEdit" class="text-slate-400 hover:scale-120 transition-transform">
                    <X :size="20" />
                  </button>
                </div>
                <div v-else class="flex justify-end gap-6 text-slate-400">
                  <Edit2 @click="startEdit(doc)" :size="18"
                    class="cursor-pointer hover:text-blue-500 transition-colors" />
                  <Trash2 @click="deactive(doc.user?.name)" :size="18"
                    class="cursor-pointer hover:text-red-500 transition-colors" />
                </div>
              </td>
            </tr>
            <tr v-if="doctors.length === 0 && !isLoading">
              <td colspan="6" class="py-20 text-center text-slate-400">
                <Search class="mx-auto mb-2 opacity-20" :size="40" />
                <p class="text-sm">No doctors found matching your criteria.</p>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <DialogueBox ref="deactiveAcc" />

      <div class="px-6 py-4 border-t border-slate-100 flex items-center justify-between bg-white">
        <div class="text-sm text-slate-500 font-medium">
          Showing <span class="text-slate-900 font-bold">{{ ((currentPage - 1) * 10) + 1 }} - {{ Math.min(currentPage *
            10, totalRecords) }}</span> of {{ totalRecords }}
        </div>
        <div class="flex items-center gap-2">
          <button @click="prevPage" :disabled="currentPage === 1"
            class="p-2 rounded-lg border border-slate-200 disabled:opacity-30 hover:bg-slate-50 transition-colors">
            <ChevronLeft :size="18" />
          </button>
          <div class="flex gap-1">
            <button v-for="p in pages" :key="p" @click="currentPage = p" :class="[
              'px-3.5 py-1.5 text-sm font-bold rounded-lg transition-all',
              currentPage === p
                ? 'bg-blue-600 text-white shadow-md shadow-blue-200'
                : 'text-slate-500 hover:bg-slate-50'
            ]">
              {{ p }}
            </button>
          </div>
          <button @click="nextPage" :disabled="currentPage >= totalPages"
            class="p-2 rounded-lg border border-slate-200 disabled:opacity-30 hover:bg-slate-50 transition-colors">
            <ChevronRight :size="18" />
          </button>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mx-10">
      <div v-for="stat in stats" :key="stat.title"
        class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm flex items-center gap-4 transition-transform hover:translate-y-0.5">
        <div :class="['p-4 rounded-2xl', stat.bg]">
          <component :is="stat.icon" :class="stat.color" :size="24" />
        </div>
        <div>
          <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">{{ stat.title }}</p>
          <p class="text-2xl font-bold text-slate-800">{{ stat.value }}</p>
        </div>
      </div>
    </div>
  </div>
</template>