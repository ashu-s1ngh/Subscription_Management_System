import Link from "next/link";
import { ArrowRight, ShieldCheck, RefreshCw, BarChart3, Layers } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-slate-900 text-white flex flex-col justify-between">
      <header className="px-8 py-6 flex justify-between items-center border-b border-slate-800">
        <div className="text-2xl font-bold tracking-tight text-sky-400">BRIGHTLOOP</div>
        <div className="flex gap-4">
          <Link href="/login" className="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 transition">
            Login
          </Link>
          <Link href="/register" className="px-4 py-2 rounded-lg bg-sky-500 hover:bg-sky-400 transition font-medium">
            Get Started
          </Link>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-20 text-center">
        <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight leading-tight">
          Manage subscriptions, recurring billing & revenue in one place.
        </h1>
        <p className="mt-6 text-xl text-slate-400 max-w-2xl mx-auto">
          Brightloop automates your entire subscription lifecycle—from quotation to recurring invoice, discounts, taxes, and real-time MRR analytics.
        </p>
        <div className="mt-10 flex justify-center gap-4">
          <Link href="/register" className="px-6 py-3 rounded-xl bg-sky-500 hover:bg-sky-400 font-semibold flex items-center gap-2">
            Start Free Trial <ArrowRight className="w-5 h-5" />
          </Link>
          <Link href="/login" className="px-6 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 font-medium">
            View Live Demo
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-20 text-left">
          <div className="p-6 rounded-2xl bg-slate-800/60 border border-slate-700/50">
            <RefreshCw className="w-8 h-8 text-sky-400 mb-4" />
            <h3 className="text-xl font-semibold mb-2">Automated Billing</h3>
            <p className="text-slate-400 text-sm">Eliminate spreadsheet errors with automated recurring invoice generation and cycle management.</p>
          </div>
          <div className="p-6 rounded-2xl bg-slate-800/60 border border-slate-700/50">
            <Layers className="w-8 h-8 text-sky-400 mb-4" />
            <h3 className="text-xl font-semibold mb-2">Flexible Plans</h3>
            <p className="text-slate-400 text-sm">Configure base products, add-on variants, custom frequencies, pause, and renewal rules with ease.</p>
          </div>
          <div className="p-6 rounded-2xl bg-slate-800/60 border border-slate-700/50">
            <BarChart3 className="w-8 h-8 text-sky-400 mb-4" />
            <h3 className="text-xl font-semibold mb-2">Real-time Analytics</h3>
            <p className="text-slate-400 text-sm">Track MRR, ARR, active subscribers, overdue invoices, and cash flow in an instant.</p>
          </div>
        </div>
      </main>

      <footer className="text-center py-6 text-slate-500 text-sm border-t border-slate-800">
        © 2026 Brightloop. All rights reserved.
      </footer>
    </div>
  );
}
