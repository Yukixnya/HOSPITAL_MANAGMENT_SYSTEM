<script setup>
import { ref } from 'vue';
import { 
  ChevronDown, Filter, Download, Edit2, Trash2, 
  MoreVertical, UserCheck, UserPlus, ClipboardList, 
  ChevronLeft, ChevronRight 
} from 'lucide-vue-next';

// State for filters
const selectedDepartment = ref('All Departments');
const selectedStatus = ref('All Statuses');

// Mock Data for the Table
const doctors = ref([
  { id: 'DOC-08241', name: 'Dr. Sarah Johnson', role: 'Senior Consultant', specialty: 'Cardiology', schedule: 'Mon, Wed, Fri', time: '09:00 AM - 04:00 PM', experience: '12 Years', status: 'Active', img: 'https://i.pravatar.cc/150?u=1' },
  { id: 'DOC-08242', name: 'Dr. Michael Chen', role: 'Chief of Surgery', specialty: 'Neurology', schedule: 'Tue, Thu, Sat', time: '08:00 AM - 02:00 PM', experience: '15 Years', status: 'On Leave', img: 'https://i.pravatar.cc/150?u=2' },
  { id: 'DOC-08245', name: 'Dr. Emily Davis', role: 'Resident Physician', specialty: 'Pediatrics', schedule: 'Daily', time: '07:00 AM - 03:00 PM', experience: '4 Years', status: 'Active', initials: 'ED' },
  { id: 'DOC-08249', name: 'Dr. Robert Brown', role: 'Specialist', specialty: 'Oncology', schedule: 'Mon - Fri', time: '10:00 AM - 06:00 PM', experience: '8 Years', status: 'Inactive', initials: 'RB' },
]);

const stats = [
  { title: 'TOTAL REGISTERED', value: '154', icon: UserCheck, color: 'text-blue-600', bg: 'bg-blue-50' },
  { title: 'ON DUTY NOW', value: '42', icon: UserPlus, color: 'text-emerald-600', bg: 'bg-emerald-50' },
  { title: 'PENDING PROFILES', value: '3', icon: ClipboardList, color: 'text-orange-600', bg: 'bg-orange-50' },
];

const getStatusClass = (status) => {
  switch (status) {
    case 'Active': return 'bg-emerald-50 text-emerald-600';
    case 'On Leave': return 'bg-orange-50 text-orange-600';
    case 'Inactive': return 'bg-slate-100 text-slate-500';
    default: return 'bg-gray-50 text-gray-600';
  }
};
</script>

<template>
  <div class="p-8 bg-slate-50 min-h-screen font-sans">
    
    <div class="flex flex-wrap items-end justify-between gap-4 mb-6">
      <div class="flex gap-4">
        <div class="space-y-1.5">
          <label class="text-[10px] font-bold text-slate-400 uppercase tracking-wider ml-1">Department</label>
          <div class="relative w-48">
            <select 
              v-model="selectedDepartment"
              class="w-full appearance-none bg-white border border-slate-200 rounded-xl px-4 py-2 text-sm text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all cursor-pointer"
            >
              <option>All Departments</option>
              <option>Cardiology</option>
              <option>Neurology</option>
              <option>Pediatrics</option>
              <option>Oncology</option>
            </select>
            <ChevronDown class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" :size="16" />
          </div>
        </div>

        <div class="space-y-1.5">
          <label class="text-[10px] font-bold text-slate-400 uppercase tracking-wider ml-1">Status</label>
          <div class="relative w-40">
            <select 
              v-model="selectedStatus"
              class="w-full appearance-none bg-white border border-slate-200 rounded-lg px-4 py-2 text-sm text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all cursor-pointer"
            >
              <option>All Statuses</option>
              <option>Active</option>
              <option>On Leave</option>
              <option>Inactive</option>
            </select>
            <ChevronDown class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" :size="16" />
          </div>
        </div>
      </div>

      <div class="flex gap-3">
        <button class="flex items-center gap-2 px-4 py-2 bg-white border border-slate-200 rounded-lg text-sm font-semibold text-slate-600 hover:bg-slate-50 transition-colors">
          <Filter :size="16" /> More Filters
        </button>
        <button class="flex items-center gap-2 px-4 py-2 bg-white border border-slate-200 rounded-lg text-sm font-semibold text-slate-600 hover:bg-slate-50 transition-colors">
          <Download :size="16" /> Export
        </button>
      </div>
    </div>

    <div class="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden mb-8">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="text-[11px] font-bold text-slate-400 uppercase tracking-widest border-b border-slate-50">
            <th class="px-6 py-4">Doctor Name</th>
            <th class="px-6 py-4">Specialization</th>
            <th class="px-6 py-4">Schedule</th>
            <th class="px-6 py-4">Experience</th>
            <th class="px-6 py-4">Status</th>
            <th class="px-6 py-4 text-right">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-50">
          <tr v-for="doc in doctors" :key="doc.id" class="hover:bg-slate-50/50 transition-colors">
            <td class="px-6 py-4">
              <div class="flex items-center gap-3">
                <div v-if="doc.img" class="w-10 h-10 rounded-full overflow-hidden border border-slate-100">
                  <img :src="doc.img" class="w-full h-full object-cover" />
                </div>
                <div v-else class="w-10 h-10 rounded-full bg-blue-50 text-blue-600 flex items-center justify-center font-bold text-xs border border-blue-100">
                  {{ doc.initials }}
                </div>
                <div>
                  <p class="font-bold text-slate-800 text-sm">{{ doc.name }}</p>
                  <p class="text-[11px] text-slate-400 font-medium tracking-tight">ID: {{ doc.id }}</p>
                </div>
              </div>
            </td>
            <td class="px-6 py-4">
              <p class="text-sm text-slate-700 font-medium">{{ doc.specialty }}</p>
              <p class="text-[11px] text-slate-400 italic">{{ doc.role }}</p>
            </td>
            <td class="px-6 py-4">
              <p class="text-sm text-slate-700 font-medium">{{ doc.schedule }}</p>
              <p class="text-[11px] text-slate-400">{{ doc.time }}</p>
            </td>
            <td class="px-6 py-4 text-sm text-slate-600 font-medium">
              {{ doc.experience }}
            </td>
            <td class="px-6 py-4">
              <span :class="['px-3 py-1 rounded-full text-[11px] font-bold flex items-center gap-1.5 w-fit', getStatusClass(doc.status)]">
                <span class="w-1.5 h-1.5 rounded-full bg-current"></span>
                {{ doc.status }}
              </span>
            </td>
            <td class="px-6 py-4 text-right">
              <div class="flex justify-end gap-2 text-slate-400">
                <button class="p-1.5 hover:text-blue-600 hover:bg-blue-50 rounded-md transition-colors"><Edit2 :size="16" /></button>
                <button class="p-1.5 hover:text-red-600 hover:bg-red-50 rounded-md transition-colors"><Trash2 :size="16" /></button>
                <button class="p-1.5 hover:text-slate-800 hover:bg-slate-100 rounded-md transition-colors"><MoreVertical :size="16" /></button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <div class="px-6 py-4 border-t border-slate-50 flex items-center justify-between">
        <p class="text-xs text-slate-400 font-medium">Showing <span class="text-slate-800">1 to 4</span> of 154 doctors</p>
        <div class="flex items-center gap-1">
          <button class="p-2 text-slate-400 hover:text-slate-600"><ChevronLeft :size="18" /></button>
          <button class="w-8 h-8 rounded-md bg-blue-600 text-white text-xs font-bold">1</button>
          <button v-for="p in [2, 3]" :key="p" class="w-8 h-8 rounded-md text-slate-500 text-xs font-bold hover:bg-slate-100">{{ p }}</button>
          <span class="px-1 text-slate-300">...</span>
          <button class="w-8 h-8 rounded-md text-slate-500 text-xs font-bold hover:bg-slate-100">16</button>
          <button class="p-2 text-slate-400 hover:text-slate-600"><ChevronRight :size="18" /></button>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div v-for="stat in stats" :key="stat.title" class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm flex items-center gap-5">
        <div :class="[stat.bg, stat.color, 'p-3 rounded-2xl']">
          <component :is="stat.icon" :size="24" />
        </div>
        <div>
          <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">{{ stat.title }}</p>
          <h3 class="text-2xl font-bold text-slate-800">{{ stat.value }}</h3>
        </div>
      </div>
    </div>
  </div>
</template>