'use client';

import { ResourceKind } from '../lib/api';

interface Props {
  initialKind?: ResourceKind | '';
  initialQuery?: string;
  initialTag?: string;
  initialOwner?: string;
}

export function ResourceFilterBar({ initialKind = '', initialQuery = '', initialTag = '', initialOwner = '' }: Props) {
  return (
    <form
      className="grid gap-4 rounded-xl border border-slate-800 bg-slate-900/60 p-4 md:grid-cols-4"
      method="get"
      action="/browse"
    >
      <label className="flex flex-col text-xs uppercase tracking-wide text-slate-400">
        Kind
        <select
          name="kind"
          defaultValue={initialKind}
          className="mt-2 rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100 focus:border-primary-400 focus:outline-none"
        >
          <option value="">All</option>
          <option value="app">Apps</option>
          <option value="dataset">Datasets</option>
          <option value="model">Models</option>
        </select>
      </label>
      <label className="flex flex-col text-xs uppercase tracking-wide text-slate-400">
        Search
        <input
          type="search"
          name="q"
          defaultValue={initialQuery}
          placeholder="Name, description, tags..."
          className="mt-2 rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100 focus:border-primary-400 focus:outline-none"
        />
      </label>
      <label className="flex flex-col text-xs uppercase tracking-wide text-slate-400">
        Tag
        <input
          name="tag"
          defaultValue={initialTag}
          className="mt-2 rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100 focus:border-primary-400 focus:outline-none"
        />
      </label>
      <label className="flex flex-col text-xs uppercase tracking-wide text-slate-400">
        Owner
        <input
          name="owner"
          defaultValue={initialOwner}
          className="mt-2 rounded-md border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100 focus:border-primary-400 focus:outline-none"
        />
      </label>
      <div className="md:col-span-4 flex justify-end gap-3 pt-2 text-sm">
        <a
          href="/browse"
          className="rounded-md border border-slate-700 px-4 py-2 font-semibold text-slate-200 hover:border-primary-400 hover:text-primary-200"
        >
          Reset
        </a>
        <button
          type="submit"
          className="rounded-md bg-primary-600 px-4 py-2 font-semibold text-white hover:bg-primary-500"
        >
          Apply
        </button>
      </div>
    </form>
  );
}
