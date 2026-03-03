<script setup>
import { ref } from 'vue';
import { 
  AlertTriangleIcon, EditIcon, DownloadIcon, CalendarIcon, HeartIcon, ActivityIcon, ScaleIcon,
  HistoryIcon, StethoscopeIcon, SyringeIcon, ScanIcon, FilePlusIcon, ClipboardCheckIcon, PlusSquareIcon
} from 'lucide-vue-next';

const quickStats = [
  { label: 'Last Visit', value: 'Oct 12,', unit: '2023', icon: CalendarIcon, iconClass: 'text-blue-500' },
  { label: 'Heart Rate', value: '72', unit: 'bpm', icon: HeartIcon, iconClass: 'text-red-500' },
  { label: 'Blood Pressure', value: '120/80', unit: 'mmHg', icon: ActivityIcon, iconClass: 'text-blue-400' },
  { label: 'BMI', value: '24.5', unit: 'Normal', icon: ScaleIcon, iconClass: 'text-green-500' },
];

const timeline = [
  { date: 'Oct 12, 2023', title: 'General Checkup', desc: 'Patient reported mild fatigue. Routine bloodwork ordered.', icon: StethoscopeIcon, iconBg: 'bg-blue-600' },
  { date: 'Aug 22, 2023', title: 'Flu Vaccination', desc: 'Administered annual flu shot (Standard dose).', icon: SyringeIcon, iconBg: 'bg-slate-300' },
  { date: 'May 15, 2023', title: 'Chest X-Ray', desc: 'Diagnostic imaging for persistent cough. Results: Clear.', icon: ScanIcon, iconBg: 'bg-slate-300' },
];

const labs = [
  { name: 'Hemoglobin A1c', result: '5.4%', range: '4.0 - 5.6%', trend: 4, trendColor: 'bg-blue-500' },
  { name: 'LDL Cholesterol', result: '115 mg/dL', range: '< 100 mg/dL', status: 'alert', trend: 4, trendColor: 'bg-orange-500' },
  { name: 'TSH', result: '2.1 mIU/L', range: '0.4 - 4.0 mIU/L', trend: 3, trendColor: 'bg-blue-400' },
];

const medications = [
  { name: 'Lisinopril 10mg', reason: 'Prescribed for: Hypertension', schedule: 'DAILY', progress: 40, taken: 12, total: 30 },
  { name: 'Atorvastatin 20mg', reason: 'Prescribed for: High Cholesterol', schedule: 'NIGHTLY', progress: 85, taken: 26, total: 30 },
  { name: 'Metformin 500mg', reason: 'Prescribed for: Blood Sugar Management', schedule: 'BID', progress: 40, taken: 12, total: 30 },
];
</script>

<template>
  <div class="min-h-screen bg-gray-50 p-4 md:p-8 font-sans text-slate-700">
    <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 mb-8">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        <div class="flex items-center gap-6">
          <div class="relative">
            <img src="https://i.pravatar.cc/150?u=1" class="w-20 h-20 rounded-full border-4 border-white shadow-md object-cover" />
            <span class="absolute bottom-1 right-1 w-5 h-5 bg-green-500 border-4 border-white rounded-full"></span>
          </div>
          <div>
            <h1 class="text-3xl font-bold text-slate-900">John Doe</h1>
            <div class="flex flex-wrap items-center gap-3 mt-1 text-slate-500 text-sm font-medium">
              <span>45 years old</span>
              <span class="text-gray-300">•</span>
              <span>Male</span>
              <span class="text-gray-300">•</span>
              <span>Blood Type: <span class="text-blue-600 font-bold">O+</span></span>
            </div>
            <div class="mt-3 inline-flex items-center gap-2 bg-red-50 text-red-600 px-3 py-1 rounded-lg text-[10px] font-black uppercase tracking-wider">
              <AlertTriangleIcon class="w-3.5 h-3.5" />
              Allergies: Penicillin (High Alert)
            </div>
          </div>
        </div>
        <div class="flex gap-3 w-full md:w-auto">
          <button class="flex-1 md:flex-none px-6 py-2.5 bg-white border border-gray-200 rounded-xl text-sm font-bold hover:bg-gray-50 flex items-center justify-center gap-2">
            <EditIcon class="w-4 h-4" /> Edit Profile
          </button>
          <button class="flex-1 md:flex-none px-6 py-2.5 bg-blue-600 text-white rounded-xl text-sm font-bold shadow-md hover:bg-blue-700 flex items-center justify-center gap-2">
            <DownloadIcon class="w-4 h-4" /> Download EHR
          </button>
        </div>
      </div>

      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8 pt-8 border-t border-gray-50">
        <div v-for="stat in quickStats" :key="stat.label" class="p-4 bg-gray-50/50 rounded-2xl border border-gray-100">
          <div class="flex items-center gap-3 mb-2">
            <component :is="stat.icon" :class="stat.iconClass" class="w-5 h-5" />
            <span class="text-[10px] font-black uppercase text-slate-400 tracking-widest">{{ stat.label }}</span>
          </div>
          <div class="flex items-baseline gap-1">
            <span class="text-xl font-bold">{{ stat.value }}</span>
            <span class="text-[10px] font-bold text-slate-400">{{ stat.unit }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2 space-y-8">
        
        <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <div class="flex justify-between items-center mb-8">
            <h2 class="text-lg font-bold flex items-center gap-2">
              <HistoryIcon class="w-5 h-5 text-blue-500" /> Medical History Timeline
            </h2>
            <button class="text-blue-600 text-xs font-bold hover:underline">View All</button>
          </div>
          
          <div class="space-y-8 relative before:absolute before:left-4.75 before:top-2 before:bottom-2 before:w-0.5 before:bg-gray-100">
            <div v-for="event in timeline" :key="event.date" class="relative pl-12">
              <div :class="event.iconBg" class="absolute left-0 w-10 h-10 rounded-full border-4 border-white shadow-sm flex items-center justify-center z-10">
                <component :is="event.icon" class="w-4 h-4 text-white" />
              </div>
              <div>
                <p class="text-[10px] font-black uppercase text-slate-400 mb-1">{{ event.date }}</p>
                <h3 class="text-sm font-bold text-slate-900">{{ event.title }}</h3>
                <p class="text-sm text-slate-500 mt-1 leading-relaxed">{{ event.desc }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-lg font-bold flex items-center gap-2">
              <ActivityIcon class="w-5 h-5 text-blue-500" /> Recent Lab Results
            </h2>
            <button class="text-blue-600 text-xs font-bold hover:underline">Full Reports</button>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left">
              <thead>
                <tr class="text-[10px] font-black uppercase text-slate-400 tracking-widest border-b border-gray-50">
                  <th class="pb-4">Test Name</th>
                  <th class="pb-4">Result</th>
                  <th class="pb-4">Reference Range</th>
                  <th class="pb-4">Trend</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-50">
                <tr v-for="lab in labs" :key="lab.name">
                  <td class="py-4 text-sm font-bold text-slate-900">{{ lab.name }}</td>
                  <td class="py-4 text-sm font-bold" :class="lab.status === 'alert' ? 'text-orange-600' : 'text-green-600'">{{ lab.result }}</td>
                  <td class="py-4 text-xs text-slate-400 font-medium">{{ lab.range }}</td>
                  <td class="py-4">
                    <div class="flex gap-1">
                      <div v-for="i in 5" :key="i" :class="[i <= lab.trend ? lab.trendColor : 'bg-gray-100']" class="w-4 h-2 rounded-sm"></div>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="space-y-6">
        <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <h2 class="text-lg font-bold mb-4">Quick Actions</h2>
          <div class="space-y-3">
            <button class="w-full flex items-center gap-3 p-3 rounded-xl bg-blue-50 text-blue-700 font-bold text-sm hover:bg-blue-100 transition-colors">
              <FilePlusIcon class="w-4 h-4" /> Add Clinical Note
            </button>
            <button class="w-full flex items-center gap-3 p-3 rounded-xl bg-green-50 text-green-700 font-bold text-sm hover:bg-green-100 transition-colors">
              <ClipboardCheckIcon class="w-4 h-4" /> New Prescription
            </button>
            <button class="w-full flex items-center gap-3 p-3 rounded-xl bg-slate-50 text-slate-700 font-bold text-sm hover:bg-slate-100 transition-colors">
              <CalendarIcon class="w-4 h-4" /> Book Follow-up
            </button>
          </div>
        </div>

        <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-lg font-bold flex items-center gap-2">
              <PlusSquareIcon class="w-5 h-5 text-blue-500" /> Active Medications
            </h2>
            <span class="bg-blue-100 text-blue-700 text-[10px] font-black px-2 py-0.5 rounded">3 ACTIVE</span>
          </div>
          <div class="space-y-6">
            <div v-for="med in medications" :key="med.name">
              <div class="flex justify-between mb-1">
                <p class="text-sm font-bold text-slate-900">{{ med.name }}</p>
                <span class="text-[10px] font-black text-slate-400 uppercase tracking-tighter">{{ med.schedule }}</span>
              </div>
              <p class="text-[10px] text-slate-500 mb-2">{{ med.reason }}</p>
              <div class="h-1.5 w-full bg-gray-100 rounded-full overflow-hidden">
                <div :style="{ width: med.progress + '%' }" class="h-full bg-blue-600 rounded-full"></div>
              </div>
              <div class="flex justify-between mt-1 text-[9px] font-bold text-slate-400">
                <span>{{ med.taken }} days</span>
                <span>{{ med.total }} days</span>
              </div>
            </div>
            <button class="w-full text-center text-xs font-bold text-slate-400 hover:text-blue-600 mt-4">View Full Prescription List</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

