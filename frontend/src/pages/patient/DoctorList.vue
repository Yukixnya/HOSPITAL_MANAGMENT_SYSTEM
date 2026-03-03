<script setup>
import { ref, computed } from 'vue';
import router from '../../router';

const searchQuery = ref('');
const activeFilters = ref(['Cardiology', 'This Week']);

const removeFilter = (filter) => {
  activeFilters.value = activeFilters.value.filter(f => f !== filter);
};

const doctors = [
  {
    id: 1,
    name: 'Dr. Sarah Smith',
    specialty: 'Senior Cardiologist',
    clinic: 'Central Medical Hospital',
    rating: 4.9,
    reviews: 120,
    fee: 120.00,
    online: true,
    bio: 'Expert in non-invasive cardiology and preventive heart care with over 12 years of experience.',
    image: 'https://i.pravatar.cc/150?u=sarah'
  },
  {
    id: 2,
    name: 'Dr. Marcus Chen',
    specialty: 'Neurologist',
    clinic: 'Neuroscience Center',
    rating: 4.8,
    reviews: 85,
    fee: 150.00,
    online: false,
    bio: 'Specializing in cognitive disorders and neurological rehabilitation. Research focus on sleep apnea.',
    image: 'https://i.pravatar.cc/150?u=marcus'
  },
  {
    id: 3,
    name: 'Dr. Elena Rodriguez',
    specialty: 'Pediatrician',
    clinic: 'Kindercare Clinic',
    rating: 5.0,
    reviews: 210,
    fee: 95.00,
    online: true,
    bio: 'Dedicated to providing compassionate care for children and adolescents for over 15 years.',
    image: 'https://i.pravatar.cc/150?u=elena'
  }
];

const filteredDoctors = computed(() => {
  if (!searchQuery.value) return doctors;
  const q = searchQuery.value.toLowerCase();
  return doctors.filter(d => 
    d.name.toLowerCase().includes(q) || 
    d.specialty.toLowerCase().includes(q) || 
    d.clinic.toLowerCase().includes(q)
  );
});
</script>

<template>
  <div class="max-w-7xl mx-auto space-y-8 p-4 md:p-8 font-sans text-slate-900 bg-[#F8FAFC] min-h-screen">
    <header class="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
      <div class="max-w-xl">
        <h1 class="text-3xl font-bold text-slate-900">Find a Healthcare Specialist</h1>
        <p class="text-slate-500 mt-2">Discover and book appointments with 250+ certified medical professionals.</p>
      </div>
      
      <div class="flex-1 max-w-2xl relative group">
        <span class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 transition-colors group-focus-within:text-blue-500">🔍</span>
        <input 
          v-model="searchQuery"
          type="text" 
          placeholder="Search by name, clinic, or specialty..." 
          class="w-full pl-12 pr-12 py-4 bg-white border border-slate-100 rounded-2xl shadow-sm focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 outline-none transition-all"
        />
        <button class="absolute right-4 top-1/2 -translate-y-1/2 p-1 hover:bg-slate-100 rounded-lg transition">
          <span class="text-slate-400">⚖️</span>
        </button>
      </div>
    </header>

    <section class="flex flex-wrap items-center justify-between gap-4 border-b border-slate-100 pb-6">
      <div class="flex flex-wrap gap-3 items-center">
        <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest mr-2">Results For:</span>
        <div v-for="filter in activeFilters" :key="filter" class="flex items-center gap-2 bg-white border border-slate-200 px-3 py-1.5 rounded-full text-xs font-bold text-slate-600">
          {{ filter }}
          <button @click="removeFilter(filter)" class="hover:text-red-500 transition text-sm">×</button>
        </div>
      </div>
      <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest">
        Showing {{ filteredDoctors.length }} Doctors
      </p>
    </section>

    <main class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="doc in filteredDoctors" :key="doc.id" class="bg-white p-8 rounded-4xl border border-slate-100 shadow-sm hover:shadow-xl hover:border-blue-100 transition-all duration-300 flex flex-col group">
        <div class="flex items-start justify-between mb-6">
          <div class="relative">
            <img :src="doc.image" class="w-20 h-20 rounded-2xl object-cover bg-slate-100 border border-slate-50 shadow-inner" />
            <div :class="doc.online ? 'bg-green-500' : 'bg-slate-300'" class="absolute -bottom-1 -right-1 w-4 h-4 rounded-full border-4 border-white"></div>
          </div>
          <div class="text-right">
            <div class="flex items-center justify-end gap-1 text-yellow-400">
              <span class="text-sm">★</span>
              <span class="text-slate-900 font-bold text-sm">{{ doc.rating }}</span>
            </div>
            <p class="text-[10px] font-black text-slate-400 uppercase tracking-tighter mt-1">{{ doc.reviews }} Reviews</p>
          </div>
        </div>

        <div class="mb-4">
          <h3 class="text-lg font-bold text-slate-900 group-hover:text-blue-600 transition">{{ doc.name }}</h3>
          <p class="text-[10px] font-black text-blue-600 uppercase tracking-widest mt-1">{{ doc.specialty }}</p>
        </div>

        <div class="flex items-center gap-2 text-xs text-slate-400 mb-6">
          <span>📍</span>
          <span>{{ doc.clinic }}</span>
        </div>

        <p class="text-sm text-slate-500 leading-relaxed mb-8 flex-1 line-clamp-2">
          {{ doc.bio }}
        </p>

        <div class="flex items-center justify-between pt-6 border-t border-slate-50">
          <div>
            <p class="text-[10px] font-black text-slate-400 uppercase tracking-tighter mb-1">Consultation</p>
            <p class="text-xl font-black text-slate-900">${{ doc.fee.toFixed(2) }}</p>
          </div>
          <button @click="() => router.push(`/patient/doctors/${doc.id}`)" class="bg-[#2563eb] text-white px-6 py-3 rounded-xl font-bold text-sm hover:bg-blue-700 transition shadow-lg shadow-blue-500/20 active:scale-95">
            View Profile
          </button>
        </div>
      </div>
    </main>

    <nav class="flex justify-center items-center gap-2 pt-10">
      <button class="w-10 h-10 flex items-center justify-center border border-slate-200 rounded-xl text-slate-400 hover:bg-white">‹</button>
      <button v-for="page in [1, 2, 3]" :key="page" 
              :class="page === 1 ? 'bg-blue-600 text-white shadow-lg shadow-blue-200' : 'bg-white text-slate-600 border border-slate-200'"
              class="w-10 h-10 flex items-center justify-center rounded-xl font-bold transition">
        {{ page }}
      </button>
      <span class="px-2 text-slate-400 font-bold">...</span>
      <button class="w-10 h-10 bg-white border border-slate-200 rounded-xl font-bold">12</button>
      <button class="w-10 h-10 flex items-center justify-center border border-slate-200 rounded-xl text-slate-400 hover:bg-white">›</button>
    </nav>
  </div>
</template>

