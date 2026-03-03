<script setup>
import { ref, computed } from 'vue';

// 1. Dynamic Date Generation Logic
const today = new Date();
const selectedDate = ref(new Date().toISOString().split('T')[0]); // Default to today
const selectedSlot = ref('10:30 AM');

const slots = ['09:00 AM', '10:30 AM', '01:00 PM', '02:30 PM', '04:00 PM', '05:30 PM'];

const doctor = {
    name: 'Dr. Sarah Smith',
    image: 'https://i.pravatar.cc/150?u=sarah',
    title: 'Senior Consultant Cardiologist',
    education: 'MD, Ph.D. - Harvard Medical',
    experience: '15+ Years',
    languages: ['English', 'Spanish', 'French'],
    rating: 4.9,
    patientCount: '2.5k+',
    reviews: '120+',
    fee: 150,
    specializations: ['Interventional Cardiology', 'Heart Failure Management', 'Cardiovascular Imaging', 'Preventive Care', 'Hypertension Treatment'],
    bio_p1: 'Dr. Sarah Smith is a world-renowned cardiologist specializing in preventive medicine and complex cardiovascular procedures. With over 15 years of practice at top-tier medical institutions, she has pioneered several minimally invasive techniques for heart valve repairs.',
    bio_p2: 'She is dedicated to patient-centric care, focusing on holistic well-being alongside advanced clinical treatments. Her research in heart failure management has been published in numerous international medical journals.'
};

const reviews = [
    {
        id: 1,
        author: 'Michael R.',
        rating: 5,
        date: '2 days ago',
        comment: 'Dr. Smith was incredibly thorough and explained everything in a way I could understand. Highly recommended.'
    },
    {
        id: 2,
        author: 'Elena K.',
        rating: 5,
        date: '1 week ago',
        comment: 'The care and attention I received were exceptional. She really takes her time with patients.'
    }
];

// Compute the next 15 days starting from today
const next15Days = computed(() => {
    const dates = [];
    for (let i = 0; i < 15; i++) {
        const d = new Date();
        d.setDate(today.getDate() + i);
        dates.push({
            fullDate: d.toISOString().split('T')[0],
            dayNum: d.getDate(),
            weekday: d.toLocaleDateString('en-US', { weekday: 'short' }).substring(0, 2),
            isToday: i === 0
        });
    }
    return dates;
});

const currentMonthDisplay = computed(() => {
    return today.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
});

const handleBooking = () => {
    const formattedDate = new Date(selectedDate.value).toLocaleDateString('en-US', {
        weekday: 'long',
        month: 'long',
        day: 'numeric'
    });
    alert(`Booking confirmed with ${doctor.name} for ${formattedDate} at ${selectedSlot.value}!`);
};
</script>

<template>
    <div class="max-w-7xl mx-auto p-4 md:p-8 font-sans text-slate-900 bg-[#F8FAFC] min-h-screen">
        <div class="grid grid-cols-12 gap-8">

            <div class="col-span-12 lg:col-span-8 space-y-8">
                <section
                    class="bg-white p-8 rounded-3xl border border-slate-100 shadow-sm flex flex-col md:flex-row gap-8 items-center md:items-start">
                    <div class="relative">
                        <img :src="doctor.image"
                            class="w-32 h-32 rounded-3xl object-cover border-4 border-white shadow-lg" />
                        <div
                            class="absolute -bottom-2 -right-2 w-6 h-6 bg-green-500 rounded-full border-4 border-white">
                        </div>
                    </div>

                    <div class="flex-1 text-center md:text-left">
                        <div class="flex flex-col md:flex-row md:items-center gap-3 mb-2">
                            <h1 class="text-3xl font-black text-slate-900">{{ doctor.name }}</h1>
                            <span
                                class="bg-blue-50 text-blue-600 px-3 py-1 rounded-lg text-[10px] font-black uppercase tracking-widest self-center md:self-auto">
                                Verified Expert
                            </span>
                        </div>
                        <p class="text-slate-500 font-bold mb-4">{{ doctor.title }}</p>

                        <div class="flex flex-wrap justify-center md:justify-start gap-6 text-sm">
                            <div class="flex items-center gap-2"><span class="text-blue-500">🎓</span> {{
                                doctor.education }}</div>
                            <div class="flex items-center gap-2"><span class="text-blue-500">💼</span> {{
                                doctor.experience }} Experience</div>
                            <div class="flex items-center gap-2"><span class="text-blue-500">🌐</span> {{
                                doctor.languages.join(', ') }}</div>
                        </div>

                        <div class="grid grid-cols-3 gap-4 mt-8">
                            <div class="bg-slate-50 p-4 rounded-2xl text-center">
                                <p class="text-xl font-black">{{ doctor.rating }}</p>
                                <p class="text-[10px] text-slate-400 font-bold uppercase">Rating</p>
                            </div>
                            <div class="bg-slate-50 p-4 rounded-2xl text-center">
                                <p class="text-xl font-black">{{ doctor.patientCount }}</p>
                                <p class="text-[10px] text-slate-400 font-bold uppercase">Patients</p>
                            </div>
                            <div class="bg-slate-50 p-4 rounded-2xl text-center">
                                <p class="text-xl font-black">{{ doctor.reviews }}</p>
                                <p class="text-[10px] text-slate-400 font-bold uppercase">Reviews</p>
                            </div>
                        </div>
                    </div>
                </section>

                <section class="bg-white p-8 rounded-3xl border border-slate-100 shadow-sm">
                    <h2 class="text-xl font-bold mb-6 flex items-center gap-2">
                        <span class="text-blue-600 text-lg">👤</span> Professional Bio
                    </h2>
                    <div class="space-y-4 text-slate-600 leading-relaxed">
                        <p>{{ doctor.bio_p1 }}</p>
                        <p>{{ doctor.bio_p2 }}</p>
                    </div>
                </section>

                <section class="bg-white p-8 rounded-3xl border border-slate-100 shadow-sm">
                    <h2 class="text-xl font-bold mb-6 flex items-center gap-2">
                        <span class="text-blue-600 text-lg">📋</span> Specializations
                    </h2>
                    <div class="flex flex-wrap gap-3">
                        <span v-for="spec in doctor.specializations" :key="spec"
                            class="bg-slate-50 border border-slate-100 px-4 py-2 rounded-xl text-xs font-bold text-slate-600">
                            {{ spec }}
                        </span>
                    </div>
                </section>
            </div>

            <div class="col-span-12 lg:col-span-4 space-y-6">
                <div class="bg-white rounded-[2.5rem] p-8 shadow-xl border border-slate-50">
                    <div class="flex justify-between items-center mb-8">
                        <h3 class="text-xl font-bold">Book Appointment</h3>
                        <p class="text-blue-600 font-black">${{ doctor.fee }}<span
                                class="text-xs text-slate-400 font-medium"> / session</span></p>
                    </div>

                    <div class="mb-8">
                        <div class="flex justify-between items-center mb-4">
                            <p class="font-bold text-sm">{{ currentMonthDisplay }}</p>
                            <div class="flex gap-2">
                                <button class="p-1 hover:bg-slate-100 rounded-lg text-slate-300">‹</button>
                                <button class="p-1 hover:bg-slate-100 rounded-lg text-slate-300">›</button>
                            </div>
                        </div>

                        <div class="grid grid-cols-5 gap-2">
                            <button v-for="date in next15Days" :key="date.fullDate"
                                @click="selectedDate = date.fullDate"
                                :class="selectedDate === date.fullDate ? 'bg-blue-600 text-white shadow-lg' : 'bg-slate-50 hover:bg-blue-50 text-slate-600'"
                                class="h-14 rounded-2xl flex flex-col items-center justify-center transition-all">
                                <span class="text-[9px] uppercase font-bold opacity-60">{{ date.weekday }}</span>
                                <span class="text-sm font-black">{{ date.dayNum }}</span>
                            </button>
                        </div>
                    </div>

                    <div class="mb-8">
                        <p class="font-bold text-sm mb-4">Available Slots</p>
                        <div class="grid grid-cols-2 gap-3">
                            <button v-for="time in slots" :key="time" @click="selectedSlot = time"
                                :class="selectedSlot === time ? 'border-blue-600 bg-blue-50 text-blue-600' : 'border-slate-100 text-slate-500'"
                                class="py-3 border-2 rounded-xl text-xs font-bold transition">
                                {{ time }}
                            </button>
                        </div>
                    </div>

                    <button @click="handleBooking"
                        class="w-full bg-[#2563eb] text-white py-4 rounded-2xl font-bold shadow-lg shadow-blue-500/20 hover:bg-blue-700 transition active:scale-95 mb-4">
                        Confirm Appointment
                    </button>
                    <p class="text-[10px] text-center text-slate-400 font-medium italic">No immediate charge. Payment
                        after consultation.</p>
                </div>

                <div class="bg-slate-50 p-6 rounded-3xl space-y-4">
                    <div class="flex items-start gap-3">
                        <span class="text-blue-500 mt-1">📍</span>
                        <div>
                            <p class="text-sm font-bold">Medical Center East</p>
                            <p class="text-xs text-slate-400">123 Health Ave, New York, NY</p>
                        </div>
                    </div>
                    <div class="flex items-start gap-3">
                        <span class="text-blue-500 mt-1">🕒</span>
                        <div>
                            <p class="text-sm font-bold">Wait Time</p>
                            <p class="text-xs text-slate-400">Average 15-20 minutes</p>
                        </div>
                    </div>
                </div>
            </div>
            <section class="bg-white col-span-8 p-8 rounded-3xl border border-slate-100 shadow-sm mt-8">
                <div class="flex items-center justify-between mb-8">
                    <h2 class="text-xl font-bold flex items-center gap-2">
                        <span class="text-blue-600 text-lg">⭐</span> Patient Reviews
                    </h2>
                    <button class="text-blue-600 font-bold text-sm hover:underline">View All</button>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div v-for="review in reviews" :key="review.id"
                        class="p-6 rounded-2xl bg-slate-50/50 border border-slate-100 hover:border-blue-100 transition-colors group">
                        <div class="flex items-center gap-3 mb-4">
                            <div
                                class="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-sm font-bold text-blue-600">
                                {{ review.author.charAt(0) }}
                            </div>
                            <div>
                                <h4 class="text-sm font-bold text-slate-900">{{ review.author }}</h4>
                                <div class="flex text-yellow-400 text-[10px]">
                                    <span v-for="n in 5" :key="n">{{ n <= review.rating ? '★' : '☆' }}</span>
                                </div>
                            </div>
                            <span class="ml-auto text-[10px] font-medium text-slate-400">{{ review.date }}</span>
                        </div>
                        <p class="text-xs text-slate-600 leading-relaxed italic">
                            "{{ review.comment }}"
                        </p>
                    </div>
                </div>
            </section>
        </div>
    </div>
</template>