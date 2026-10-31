export default function Page() {
  return (
    <div className="p-8 max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold text-slate-900 tracking-tight">My Invoices</h1>
      <p className="mt-2 text-slate-500">Download invoices and check payment balances</p>
      <div className="mt-8 p-6 bg-white border border-slate-200 rounded-xl shadow-sm">
        <p className="text-sm text-slate-600">Module ready for integration with FastAPI backend and Supabase.</p>
      </div>
    </div>
  );
}
