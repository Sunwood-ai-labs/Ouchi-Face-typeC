import { notFound } from 'next/navigation';

import { ResourceCard } from '../../../components/resource-card';
import { statusStyles } from '../../../lib/status-style';
import { fetchResourceBySlug } from '../../../lib/api';

interface Params {
  slug: string;
}

export default async function ResourceDetailPage({ params }: { params: Params }) {
  const resource = await fetchResourceBySlug(params.slug).catch(() => null);
  if (!resource) {
    notFound();
  }

  return (
    <article className="space-y-8">
      <header className="rounded-2xl border border-slate-800 bg-slate-900/70 p-8 shadow-lg shadow-slate-900/40">
        <div className="flex items-center justify-between">
          <span className="text-sm uppercase tracking-[0.3em] text-slate-400">{resource.kind}</span>
          <span className={`rounded-full px-3 py-1 text-xs font-semibold ${statusStyles(resource.health_status)}`}>
            {resource.health_status.toUpperCase()} •{' '}
            {resource.health_checked_at ? new Date(resource.health_checked_at).toLocaleString() : 'never checked'}
          </span>
        </div>
        <h1 className="mt-4 text-4xl font-bold text-slate-100">{resource.name}</h1>
        <p className="mt-3 max-w-2xl text-slate-300">{resource.description}</p>
        <div className="mt-4 flex flex-wrap gap-3 text-sm text-slate-300">
          {resource.owner ? <span className="rounded-md border border-slate-700 px-3 py-1">Owner: {resource.owner}</span> : null}
          {resource.license ? <span className="rounded-md border border-slate-700 px-3 py-1">License: {resource.license}</span> : null}
          {resource.updated_at ? (
            <span className="rounded-md border border-slate-700 px-3 py-1">
              Updated: {new Date(resource.updated_at).toLocaleDateString()}
            </span>
          ) : null}
        </div>
        <div className="mt-6 flex gap-4 text-sm">
          {resource.url ? (
            <a
              href={resource.url}
              className="rounded-md bg-primary-600 px-4 py-2 font-semibold text-white hover:bg-primary-500"
              target="_blank"
              rel="noreferrer"
            >
              Open resource
            </a>
          ) : null}
          {resource.repo_url ? (
            <a
              href={resource.repo_url}
              className="rounded-md border border-primary-500 px-4 py-2 font-semibold text-primary-200 hover:bg-primary-500/10"
              target="_blank"
              rel="noreferrer"
            >
              View repository
            </a>
          ) : null}
        </div>
      </header>

      <section className="space-y-6 rounded-2xl border border-slate-800 bg-slate-900/50 p-8">
        <h2 className="text-xl font-semibold text-slate-100">Metadata</h2>
        <dl className="grid gap-4 md:grid-cols-2">
          <div>
            <dt className="text-xs uppercase tracking-wide text-slate-400">Kind</dt>
            <dd className="mt-1 text-slate-200">{resource.kind}</dd>
          </div>
          <div>
            <dt className="text-xs uppercase tracking-wide text-slate-400">Source</dt>
            <dd className="mt-1 text-slate-200">{resource.source}</dd>
          </div>
          <div>
            <dt className="text-xs uppercase tracking-wide text-slate-400">Healthcheck path</dt>
            <dd className="mt-1 text-slate-200">{resource.healthcheck_path ?? '—'}</dd>
          </div>
          <div>
            <dt className="text-xs uppercase tracking-wide text-slate-400">Filesystem path</dt>
            <dd className="mt-1 text-slate-200">{resource.path ?? '—'}</dd>
          </div>
        </dl>
        <div>
          <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-400">Tags</h3>
          <div className="mt-2 flex flex-wrap gap-2 text-xs">
            {resource.tags.length ? (
              resource.tags.map((tag) => (
                <a
                  key={tag}
                  href={`/browse?tag=${encodeURIComponent(tag)}`}
                  className="rounded-full border border-slate-700 bg-slate-800 px-3 py-1 text-slate-200 hover:border-primary-400"
                >
                  #{tag}
                </a>
              ))
            ) : (
              <span className="text-slate-500">No tags yet.</span>
            )}
          </div>
        </div>
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-semibold text-slate-100">Quick card preview</h2>
        <ResourceCard resource={resource} />
      </section>
    </article>
  );
}
