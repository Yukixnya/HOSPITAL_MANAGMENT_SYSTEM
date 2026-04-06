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
import { useToast } from 'vue-toastification'

const toast = useToast()

// --- State Management ---
const doctors = ref([])
const currentPage = ref(1)
const totalPages = ref(1)
const totalRecords = ref(0)
const searchQuery = ref("")
const isLoading = ref(false)
let searchTimeout = null

const selectedDepartment = ref('All Departments')
const selectedStatus = ref('All Status')

const editingId = ref(null)
const editForm = ref({})
const deactiveAcc = ref(null)

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
    const isFiltering = params.search || params.status || params.specialization;

    if (isFiltering) {
      res = await filterDoctors(params);
    } else {
      res = await getDoctors(currentPage.value);
    }

    doctors.value = res.data || []
    totalPages.value = res.total_pages || 1
    totalRecords.value = res.total || 0
  } catch (error) {
    toast.error("Failed to fetch doctor list.")
  } finally {
    isLoading.value = false
  }
}

// --- Watchers ---
watch([searchQuery, selectedDepartment, selectedStatus], () => {
  currentPage.value = 1 
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => fetchDoctorList(), 400)
})

watch(currentPage, () => fetchDoctorList())
onMounted(() => fetchDoctorList())

// --- Actions ---
const startEdit = (doc) => {
  editingId.value = doc._id
  editForm.value = { 
    ...doc, 
    name: doc.name || doc.user?.name || "" 
  }
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
    toast.error("Failed to save doctor details.")
  }
}

const updateStatus = async (doc, newStatus) => {
  try {
    await updateDocStatus(doc._id, newStatus);
    doc.status = newStatus;
    toast.success(`Status updated to ${newStatus} for Dr. ${doc.name || doc.user?.name}`)
  } catch (error) {
    toast.error("Failed to update status.")
  }
}

const deactive = async (name) => {
  const ok = await deactiveAcc.value.open(`Are you sure you want to deactivate Dr. ${name}?`)
  if (ok) {
    toast.success("Doctor has been deactivated")
  }
}

// --- Helpers ---
const nextPage = () => { if (currentPage.value < totalPages.value) currentPage.value++ }
const prevPage = () => { if (currentPage.value > 1) currentPage.value-- }

const pages = computed(() => {
  const range = 1
  let start = Math.max(1, currentPage.value - range)
  let end = Math.min(totalPages.value, currentPage.value + range)
  const arr = []
  for (let i = start; i <= end; i++) arr.push(i)
  return arr
})

const getStatusStyle = (status) => {
  switch (status) {
    case 'Active': return 'status-active'
    case 'On Leave': return 'status-on-leave'
    case 'Inactive': return 'status-inactive'
    default: return ''
  }
}

const stats = computed(() => [
  { title: 'TOTAL REGISTERED', value: totalRecords.value, icon: UserCheck, color: 'icon-blue', bg: 'bg-blue-light' },
  { title: 'ON DUTY NOW', value: '42', icon: UserPlus, color: 'icon-emerald', bg: 'bg-emerald-light' },
  { title: 'PENDING PROFILES', value: '3', icon: ClipboardList, color: 'icon-orange', bg: 'bg-orange-light' },
])
</script>

<template>
  <div class="main-wrapper">
    <div class="content-container">
      <header class="page-header">
        <div class="filters-left">
          <div class="filter-group search-group">
            <label class="label-text">Search Doctor</label>
            <div class="relative-input">
              <Search class="input-icon-left" :size="18" />
              <input v-model.trim="searchQuery" type="text" placeholder="Search by name..." class="styled-input" />
            </div>
          </div>

          <div class="filter-group">
            <label class="label-text">Department</label>
            <div class="relative-input">
              <select v-model="selectedDepartment" class="styled-select">
                <option>All Departments</option>
                <option v-for="s in specializations" :key="s" :value="s">{{ s }}</option>
              </select>
              <ChevronDown class="input-icon-right" :size="18" />
            </div>
          </div>

          <div class="filter-group">
            <label class="label-text">Status</label>
            <div class="relative-input">
              <select v-model="selectedStatus" class="styled-select">
                <option>All Status</option>
                <option value="Active">Active</option>
                <option value="On Leave">On Leave</option>
                <option value="Inactive">Inactive</option>
              </select>
              <ChevronDown class="input-icon-right" :size="18" />
            </div>
          </div>
        </div>

        <button class="btn-export">
          <Download :size="18" /> Export
        </button>
      </header>

      <div class="table-card">
        <div v-if="isLoading" class="loader-overlay">
          <Loader2 class="spinner" :size="32" />
          <span class="loader-text">Syncing Data...</span>
        </div>

        <div class="table-scroll">
          <table class="data-table">
            <thead>
              <tr>
                <th>Doctor Name</th>
                <th>Specialization</th>
                <th>Schedule</th>
                <th>Experience</th>
                <th>Status</th>
                <th class="text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="doc in doctors" :key="doc._id" :class="{'is-editing': editingId === doc._id}">
                <td>
                  <div class="doc-info-flex">
                    <div class="avatar-circle">
                      {{(doc.name || doc.user?.name || '??').split(' ').map(n => n[0]).join('').toUpperCase()}}
                    </div>
                    <div>
                      <input v-if="editingId === doc._id" v-model="editForm.name" class="inline-edit-input" />
                      <p v-else class="doc-name-text">{{ doc.name || doc.user?.name }}</p>
                      <p class="doc-email-text">{{ doc.user?.email }}</p>
                    </div>
                  </div>
                </td>
                <td>
                  <select v-if="editingId === doc._id" v-model="editForm.specialization" class="inline-edit-select">
                    <option v-for="s in specializations" :key="s" :value="s">{{ s }}</option>
                  </select>
                  <span v-else class="text-medium">{{ doc.specialization }}</span>
                </td>
                <td>
                  <select v-if="editingId === doc._id" v-model="editForm.schedule" class="inline-edit-select">
                    <option v-for="s in schedules" :key="s" :value="s">{{ s }}</option>
                  </select>
                  <span v-else class="text-muted">{{ doc.schedule }}</span>
                </td>
                <td>
                  <input v-if="editingId === doc._id" type="number" v-model="editForm.experience" class="inline-edit-sm" />
                  <span v-else class="text-bold">{{ doc.experience }} Yrs</span>
                </td>
                <td>
                  <div class="status-dropdown-wrapper">
                    <select 
                      :value="doc.status" 
                      @change="updateStatus(doc, $event.target.value)" 
                      :class="['styled-status-select', getStatusStyle(doc.status)]"
                    >
                      <option value="Active">Active</option>
                      <option value="On Leave">On Leave</option>
                      <option value="Inactive">Inactive</option>
                    </select>
                  </div>
                </td>
                <td class="text-right">
                  <div v-if="editingId === doc._id" class="action-flex-right">
                    <Check @click="saveEdit" class="icon-save cursor-pointer" :size="20" />
                    <X @click="cancelEdit" class="icon-cancel cursor-pointer" :size="20" />
                  </div>
                  <div v-else class="action-flex-right">
                    <Edit2 @click="startEdit(doc)" class="icon-edit cursor-pointer" :size="18" />
                    <Trash2 @click="deactive(doc.name || doc.user?.name)" class="icon-delete cursor-pointer" :size="18" />
                  </div>
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

      <div class="stats-grid">
        <div v-for="stat in stats" :key="stat.title" class="stat-card">
          <div :class="['stat-icon-container', stat.bg]">
            <component :is="stat.icon" :class="stat.color" :size="24" />
          </div>
          <div>
            <p class="stat-label">{{ stat.title }}</p>
            <p class="stat-value">{{ stat.value }}</p>
          </div>
        </div>
      </div>
    </div>
    <DialogueBox ref="deactiveAcc" />
  </div>
</template>

<style src="../../styles/adminDoctor.css" scoped></style>