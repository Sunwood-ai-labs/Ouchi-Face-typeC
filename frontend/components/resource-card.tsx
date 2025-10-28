import Image from 'next/image';
import Link from 'next/link';

import type { Resource } from '../lib/api';
import { statusStyles } from '../lib/status-style';

interface Props {
  resource: Resource;
}

export function ResourceCard({ resource }: Props) {
  return (
    <div className="group flex flex-col rounded-xl border border-slate-800 bg-slate-900/70 p-5 shadow-lg shadow-slate-900/40 transition hover:border-primary-500/60 hover:bg-slate-900">
      <div className="flex items-center justify-between">
        <span className="text-xs uppercase tracking-widest text-slate-400">{resource.kind}</span>
        <span className={`rounded-full px-2 py-0.5 text-xs font-semibold ${statusStyles(resource.health_status)}`}>
          {resource.health_status.toUpperCase()}
        </span>
      </div>
      <h3 className="mt-3 text-lg font-semibold text-slate-100">{resource.name}</h3>
      <p className="mt-2 line-clamp-3 text-sm text-slate-300">{resource.description ?? 'No description yet.'}</p>
      {resource.thumbnail_path ? (
        <div className="mt-4 overflow-hidden rounded-lg border border-slate-800">
          <Image
            src={resource.thumbnail_path}
            alt={`${resource.name} thumbnail`}
            width={640}
            height={360}
            className="h-32 w-full object-cover"
          />
        </div>
      ) : null}
      <div className="mt-4 flex flex-wrap gap-2 text-xs">
        {resource.tags.map((tag) => (
          <span key={tag} className="rounded-full border border-slate-700 bg-slate-800 px-3 py-1 text-slate-200">
            #{tag}
          </span>
        ))}
      </div>
      <div className="mt-6 flex items-center justify-between text-sm text-primary-300">
        <Link href={`/r/${resource.slug}`} className="font-semibold hover:text-primary-200">
          View details →
        </Link>
        {resource.url ? (
          <a href={resource.url} target="_blank" rel="noreferrer" className="hover:text-primary-200">
            Open app
          </a>
        ) : null}
      </div>
    </div>
  );
}
