<script setup>
const prescriptions = [
    { name: 'Fluticasone Propionate (Flonase)', strength: '50 mcg/actuation', type: 'Nasal Spray', dosage: '2 sprays in each nostril once daily', refills: 3 },
    { name: 'Cetirizine (Zyrtec)', strength: '10 mg', type: 'Oral Tablet', dosage: '1 tablet daily in the evening', refills: 1 }
];

const notes = [
    { title: 'Next Steps', content: 'Increase fluid intake and use a saline rinse twice daily before nasal spray. Monitor for any shortness of breath.' },
    { title: 'Lifestyle Recommendation', content: 'Keep windows closed during high pollen days. Use HEPA filter in the bedroom.' },
    { title: 'Follow-Up', content: 'Schedule a review in 4 weeks if symptoms do not improve with medication.' }
];

const visitVitals = [
    { label: 'Blood Pressure', value: '122/78', unit: 'mmHg' },
    { label: 'Heart Rate', value: '72', unit: 'bpm' },
    { label: 'Temperature', value: '98.6', unit: '°F' },
    { label: 'Oxygen Sat.', value: '99', unit: '%' }
];
</script>

<template>
    <div class="max-w-7xl mx-auto mt-8 space-y-6">
        <header class="flex flex-col md:flex-row md:items-end justify-between gap-4">
            <div>
                <h1 class="text-3xl font-bold text-slate-900">Visit Summary & Results</h1>
                <p class="text-slate-500">Appointment on October 24, 2023</p>
            </div>
            <div class="flex gap-3">
                <button
                    class="bg-white border border-slate-200 px-5 py-2.5 rounded-xl font-bold text-sm flex items-center gap-2 hover:bg-slate-50 transition">
                    🖨️ Print Summary
                </button>
                <button
                    class="bg-[#2563eb] text-white px-5 py-2.5 rounded-xl font-bold text-sm flex items-center gap-2 hover:bg-blue-700 transition shadow-lg shadow-blue-500/20">
                    📥 Download PDF
                </button>
            </div>
        </header>

        <div class="grid grid-cols-12 gap-6">
            <div class="col-span-12 lg:col-span-8 space-y-6">

                <section class="bg-white p-8 rounded-4xl border border-slate-100 shadow-sm">
                    <div class="flex items-center gap-3 mb-6">
                        <div class="bg-blue-50 p-2.5 rounded-xl text-blue-600 text-xl">🏥</div>
                        <h2 class="text-xl font-bold">Primary Diagnosis</h2>
                    </div>
                    <div class="bg-slate-50/50 border border-slate-100 p-6 rounded-2xl">
                        <div class="flex justify-between items-start mb-4">
                            <div>
                                <h3 class="text-xl font-bold text-blue-600">Acute Seasonal Rhinitis</h3>
                                <p class="text-xs font-bold text-slate-400 mt-1 uppercase tracking-wider">ICD-10 Code:
                                    J30.1 • Status: Confirmed</p>
                            </div>
                        </div>
                        <p class="text-slate-600 leading-relaxed text-sm">
                            Patient presents with persistent nasal congestion, sneezing, and watery eyes. Symptoms
                            correlate with local pollen count increases. No signs of secondary bacterial infection at
                            this time.
                        </p>
                    </div>
                </section>

                <section class="bg-white p-8 rounded-4xl border border-slate-100 shadow-sm">
                    <div class="flex justify-between items-center mb-6">
                        <div class="flex items-center gap-3">
                            <div class="bg-green-50 p-2.5 rounded-xl text-green-600 text-xl">💊</div>
                            <h2 class="text-xl font-bold">Prescriptions</h2>
                        </div>
                        <span
                            class="bg-green-100 text-green-600 text-[10px] font-black px-3 py-1 rounded-full uppercase">2
                            Active</span>
                    </div>

                    <div class="space-y-4">
                        <div v-for="med in prescriptions" :key="med.name"
                            class="p-5 border border-slate-100 rounded-2xl bg-white hover:border-blue-100 transition group">
                            <div class="flex justify-between items-start">
                                <div class="flex gap-4">
                                    <div
                                        class="w-12 h-12 bg-slate-50 rounded-full flex items-center justify-center text-slate-400 group-hover:bg-blue-50 group-hover:text-blue-500 transition">
                                        💊</div>
                                    <div>
                                        <h4 class="font-bold text-slate-800">{{ med.name }}</h4>
                                        <p class="text-xs text-slate-400 font-medium">{{ med.strength }} • {{ med.type
                                            }}</p>
                                        <div class="mt-3 flex items-center gap-2 text-blue-600 text-xs font-bold">
                                            <span>ℹ️ Dosage: {{ med.dosage }}</span>
                                        </div>
                                    </div>
                                </div>
                                <div class="text-right">
                                    <p class="text-[10px] text-slate-400 font-black uppercase tracking-tighter">Refills
                                        Remaining</p>
                                    <p class="text-xl font-bold text-slate-700">{{ med.refills }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            </div>

            <div class="col-span-12 lg:col-span-4 space-y-6">

                <section class="bg-white p-8 rounded-4xl border border-slate-100 shadow-sm">
                    <div class="flex items-center gap-3 mb-8">
                        <div class="bg-purple-50 p-2.5 rounded-xl text-purple-600 text-xl">📝</div>
                        <h2 class="text-xl font-bold">Doctor's Notes</h2>
                    </div>
                    <div
                        class="space-y-8 relative before:absolute before:inset-0 before:ml-2.5 before:w-0.5 before:bg-slate-100">
                        <div v-for="note in notes" :key="note.title" class="relative pl-8">
                            <div
                                class="absolute left-0 w-5 h-5 bg-white border-2 border-slate-200 rounded-full mt-1 flex items-center justify-center">
                                <div class="w-2 h-2 bg-blue-500 rounded-full"></div>
                            </div>
                            <h4 class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">{{
                                note.title }}</h4>
                            <p class="text-xs text-slate-600 leading-relaxed">{{ note.content }}</p>
                        </div>
                    </div>
                </section>

                <section class="bg-[#11121e] p-8 rounded-4xl text-white shadow-xl">
                    <h3 class="text-lg font-bold mb-6">Your Care Provider</h3>
                    <div class="flex items-center gap-4 mb-8">
                        <img src="https://i.pravatar.cc/100?u=elena"
                            class="w-16 h-16 rounded-2xl border-2 border-slate-700" />
                        <div>
                            <p class="text-lg font-bold">Dr. Elena Rodriguez</p>
                            <p class="text-slate-400 text-sm">Internal Medicine</p>
                        </div>
                    </div>
                    <button
                        class="w-full bg-[#2563eb] text-white py-4 rounded-2xl font-bold text-sm flex items-center justify-center gap-2 hover:bg-blue-700 transition">
                        ✉️ Send Message
                    </button>
                </section>
            </div>

            <section class="col-span-12 mb-8">
                <h2 class="text-xl font-bold mb-6">Visit Vitals</h2>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div v-for="v in visitVitals" :key="v.label"
                        class="bg-white p-6 rounded-4xl border border-slate-100 shadow-sm text-center">
                        <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">{{ v.label }}
                        </p>
                        <p class="text-2xl font-black text-slate-900">
                            {{ v.value }} <span class="text-sm font-medium text-slate-400">{{ v.unit }}</span>
                        </p>
                    </div>
                </div>
            </section>
        </div>
    </div>
</template>
