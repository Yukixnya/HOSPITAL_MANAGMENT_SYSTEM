<script setup>
const historyStats = [
  { label: 'Diagnoses', value: '12', icon: '💼', bgClass: 'bg-blue-50 text-blue-600' },
  { label: 'Lab Tests', value: '34', icon: '🔬', bgClass: 'bg-green-50 text-green-600' },
  { label: 'Vaccinations', value: '8', icon: '💉', bgClass: 'bg-purple-50 text-purple-600' },
  { label: 'Archived', value: '45', icon: '📑', bgClass: 'bg-orange-50 text-orange-600' }
];

const medicalRecords = [
  {
    id: 1,
    type: 'Lab Report',
    date: 'Oct 24, 2023',
    time: '09:15 AM',
    title: 'Comprehensive Blood Panel (Annual)',
    description: 'Routine checkup including CBC, metabolic panel, and lipid profile. Results indicate normal ranges with slight elevation in HDL cholesterol.',
    provider: 'City General Lab',
    status: 'Ready',
    icon: '🔬',
    markerClass: 'text-green-600 ring-4 ring-green-50',
    tagClass: 'bg-green-50 text-green-600',
    actionLabel: 'Download PDF'
  },
  {
    id: 2,
    type: 'Clinical Visit',
    date: 'Oct 12, 2023',
    time: '02:30 PM',
    title: 'Cardiology Consultation',
    description: 'Follow-up appointment with Dr. Sarah Smith. Heart sounds normal. No new symptoms of palpitations reported. Continue current exercise regime.',
    provider: 'Heart & Wellness Clinic',
    status: 'Ready',
    icon: '🏥',
    markerClass: 'text-blue-600 ring-4 ring-blue-50',
    tagClass: 'bg-blue-50 text-blue-600',
    actionLabel: 'Notes PDF'
  },
  {
    id: 3,
    type: 'Imaging',
    date: 'Nov 05, 2023',
    time: '11:00 AM',
    title: 'MRI Scan - Lumbar Spine',
    description: 'Scan completed. Radiologist report currently being finalized by the diagnostic team.',
    provider: 'Advanced Imaging Center',
    status: 'Pending Analysis',
    icon: '☢️',
    markerClass: 'text-orange-600 ring-4 ring-orange-50',
    tagClass: 'bg-orange-50 text-orange-600',
    actionLabel: 'Download PDF'
  }
];
</script>

<template>
  <div class="max-w-7xl mx-auto p-4 md:p-8 font-sans text-slate-900 bg-[#F8FAFC] min-h-screen">
    <header class="mb-10">
      <h1 class="text-3xl font-black text-slate-900">Complete Medical History</h1>
      <p class="text-slate-500 mt-2">A chronological overview of your health journey and clinical records.</p>
    </header>

    <section class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-12">
      <div v-for="stat in historyStats" :key="stat.label" 
           class="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm flex items-center gap-4">
        <div :class="stat.bgClass" class="w-12 h-12 rounded-2xl flex items-center justify-center text-xl">
          {{ stat.icon }}
        </div>
        <div>
          <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest">{{ stat.label }}</p>
          <p class="text-2xl font-black text-slate-900">{{ stat.value }}</p>
        </div>
      </div>
    </section>

    <div class="relative space-y-8 before:absolute before:inset-0 before:ml-5 before:md:ml-8 before:w-0.5 before:bg-slate-100">
      
      <div class="relative pl-12 md:pl-20 mb-8">
        <span class="absolute left-0 bg-slate-100 text-slate-500 px-4 py-1 rounded-full text-xs font-black">2023</span>
      </div>

      <div v-for="item in medicalRecords" :key="item.id" class="relative pl-12 md:pl-20 group">
        <div :class="item.markerClass" 
             class="absolute left-0 w-10 h-10 md:w-16 md:h-16 bg-white border-4 border-white rounded-full shadow-md flex items-center justify-center text-xl z-10 ml-0 md:-ml-3 transition-transform group-hover:scale-110">
          {{ item.icon }}
        </div>

        <div class="bg-white p-6 md:p-8 rounded-4xl border border-slate-100 shadow-sm hover:shadow-md transition-shadow">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4">
            <div class="flex flex-wrap items-center gap-3">
              <span :class="item.tagClass" class="px-3 py-1 rounded-lg text-[10px] font-black uppercase tracking-widest">
                {{ item.type }}
              </span>
              <span class="text-xs font-bold text-slate-400">{{ item.date }} • {{ item.time }}</span>
            </div>
            <div class="flex gap-2">
              <button class="flex items-center gap-2 px-4 py-2 border border-slate-100 rounded-xl text-xs font-bold text-slate-500 hover:bg-slate-50">
                📄 {{ item.actionLabel }}
              </button>
              <button v-if="item.status === 'Ready'" class="px-4 py-2 bg-[#2563eb] text-white rounded-xl text-xs font-bold hover:bg-blue-700 shadow-lg shadow-blue-500/20">
                View Report
              </button>
              <button v-else disabled class="px-4 py-2 bg-slate-100 text-slate-400 rounded-xl text-xs font-bold cursor-not-allowed">
                View Details
              </button>
            </div>
          </div>

          <h3 class="text-xl font-black text-slate-900 mb-2">{{ item.title }}</h3>
          <p class="text-sm text-slate-500 leading-relaxed mb-6 max-w-3xl">
            {{ item.description }}
          </p>

          <div class="flex flex-wrap gap-6 pt-6 border-t border-slate-50">
            <div class="text-[10px] font-bold">
              <span class="text-slate-400 uppercase tracking-tighter">Provider: </span>
              <span class="text-slate-900">{{ item.provider }}</span>
            </div>
            <div class="text-[10px] font-bold">
              <span class="text-slate-400 uppercase tracking-tighter">Status: </span>
              <span :class="item.status === 'Ready' ? 'text-green-500' : 'text-orange-500'">{{ item.status }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

