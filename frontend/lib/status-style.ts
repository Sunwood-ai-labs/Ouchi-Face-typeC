export function statusStyles(status: string) {
  switch (status) {
    case 'up':
      return 'bg-emerald-500/10 text-emerald-300 border border-emerald-400/50';
    case 'down':
      return 'bg-rose-500/10 text-rose-300 border border-rose-400/50';
    default:
      return 'bg-slate-500/10 text-slate-300 border border-slate-400/40';
  }
}
