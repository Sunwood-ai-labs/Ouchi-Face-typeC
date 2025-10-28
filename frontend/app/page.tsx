import { ResourceCard } from '../components/resource-card';
import { fetchResources } from '../lib/api';

export default async function HomePage() {
  const { items } = await fetchResources({ limit: 6 });
  const running = items.filter((item) => item.health_status === 'up');

  return (
    <section className="space-y-10">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-slate-100">Welcome back 👋</h1>
        <p className="mt-2 text-slate-300">
          All your home lab apps, datasets, and models — curated and searchable in one cute dashboard.
        </p>
      </div>

      <div>
        <h2 className="text-xl font-semibold text-slate-100">Recently added</h2>
        <div className="mt-4 grid gap-6 md:grid-cols-2 xl:grid-cols-3">
          {items.map((resource) => (
            <ResourceCard key={resource.id} resource={resource} />
          ))}
        </div>
      </div>

      <div>
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold text-slate-100">Currently running</h2>
          <a href="/browse?filter=running" className="text-sm font-semibold text-primary-300 hover:text-primary-200">
            View all →
          </a>
        </div>
        <div className="mt-4 grid gap-6 md:grid-cols-2 xl:grid-cols-3">
          {running.length ? (
            running.map((resource) => <ResourceCard key={resource.id} resource={resource} />)
          ) : (
            <p className="rounded-lg border border-dashed border-slate-700 p-6 text-sm text-slate-400">
              No running resources yet. Add a healthcheck URL to get real-time status.
            </p>
          )}
        </div>
      </div>
    </section>
  );
}
