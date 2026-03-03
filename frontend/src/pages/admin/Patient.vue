<script setup>
import { ref } from 'vue';
import { 
  Search, SlidersHorizontal, ChevronLeft, ChevronRight, 
  Calendar as CalendarIcon, ChevronDown 
} from 'lucide-vue-next';

// Filter States
const searchQuery = ref('');
const selectedAgeRange = ref('All Ages');
const admissionDate = ref('');

const ageRanges = ['All Ages', 'Under 18', '18 - 45', '45 - 65', '65+'];

// Mock Data
const patients = ref([
  { name: 'John Doe', phone: '+1 (555) 001-2233', id: '#MR-49210', age: 42, gender: 'Male', admission: 'Oct 12, 2023', lastVisit: 'Nov 05, 2023', condition: 'Stable', initials: 'JD', color: 'bg-blue-50 text-blue-600' },
  { name: 'Alice Smith', phone: '+1 (555) 002-4455', id: '#MR-49211', age: 29, gender: 'Female', admission: 'Nov 02, 2023', lastVisit: 'Nov 02, 2023', condition: 'Critical', initials: 'AS', color: 'bg-purple-50 text-purple-600' },
  { name: 'Robert Wilson', phone: '+1 (555) 003-7788', id: '#MR-49215', age: 67, gender: 'Male', admission: 'Oct 28, 2023', lastVisit: 'Oct 30, 2023', condition: 'Observing', initials: 'RW', color: 'bg-orange-50 text-orange-600' },
  { name: 'Elena Martinez', phone: '+1 (555) 004-9900', id: '#MR-49222', age: 35, gender: 'Female', admission: 'Nov 06, 2023', lastVisit: 'Nov 07, 2023', condition: 'Stable', initials: 'EM', color: 'bg-emerald-50 text-emerald-600' },
  { name: 'Michael Klein', phone: '+1 (555) 005-1122', id: '#MR-49230', age: 51, gender: 'Male', admission: 'Oct 15, 2023', lastVisit: 'Nov 04, 2023', condition: 'Discharged', initials: 'MK', color: 'bg-sky-50 text-sky-600' },
]);

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
          <input 
            v-model="searchQuery" 
            type="text"
            placeholder="Search by name, ID, or phone..." 
            class="w-full pl-10 pr-4 h-11 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all"
          />
        </div>
      </div>

      <div class="w-48 space-y-1.5">
        <label class="text-[10px] font-bold text-slate-400 uppercase tracking-wider ml-1">Filter by Age</label>
        <div class="relative">
          <select 
            v-model="selectedAgeRange"
            class="w-full appearance-none h-11 pl-4 pr-10 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 cursor-pointer"
          >
            <option v-for="range in ageRanges" :key="range" :value="range">{{ range }}</option>
          </select>
          <ChevronDown class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" :size="16" />
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
              <th class="px-6 py-5 text-right">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-50">
            <tr v-for="patient in patients" :key="patient.id" class="hover:bg-slate-50/50 transition-colors group">
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div :class="[patient.color, 'w-10 h-10 rounded-full flex items-center justify-center font-bold text-xs border border-current/10 shadow-sm']">
                    {{ patient.initials }}
                  </div>
                  <div>
                    <p class="font-bold text-slate-800 text-sm leading-tight">{{ patient.name }}</p>
                    <p class="text-[11px] text-slate-400 font-medium mt-0.5">{{ patient.phone }}</p>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4">
                <span class="text-sm font-medium text-slate-600 bg-slate-50 px-2 py-1 rounded-md">{{ patient.id }}</span>
              </td>
              <td class="px-6 py-4">
                <span class="text-sm text-slate-600 font-medium">{{ patient.age }} / {{ patient.gender }}</span>
              </td>
              <td class="px-6 py-4 text-sm text-slate-500">{{ patient.admission }}</td>
              <td class="px-6 py-4 text-sm text-slate-500">{{ patient.lastVisit }}</td>
              <td class="px-6 py-4 text-center">
                <span :class="[getConditionClass(patient.condition), 'text-[10px] font-bold px-3 py-1 rounded-full uppercase tracking-tight inline-block min-w-20 text-center shadow-sm border border-current/5']">
                  {{ patient.condition }}
                </span>
              </td>
              <td class="px-6 py-4 text-right">
                <button class="text-blue-600 text-sm font-bold hover:text-blue-700 hover:underline transition-all">
                  View Profile
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="px-6 py-5 border-t border-slate-50 flex items-center justify-between bg-white">
        <p class="text-xs text-slate-400 font-medium">
          Showing <span class="text-slate-800 font-bold">1 to 5</span> of 2,482 records
        </p>
        <div class="flex items-center gap-2">
          <button class="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-50 rounded-lg transition-colors">
            <ChevronLeft :size="18" />
          </button>
          <div class="flex gap-1">
            <button class="w-8 h-8 rounded-lg bg-blue-600 text-white text-xs font-bold shadow-md shadow-blue-200">1</button>
            <button class="w-8 h-8 rounded-lg text-slate-500 hover:bg-slate-100 text-xs font-bold transition-colors">2</button>
            <button class="w-8 h-8 rounded-lg text-slate-500 hover:bg-slate-100 text-xs font-bold transition-colors">3</button>
          </div>
          <button class="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-50 rounded-lg transition-colors">
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