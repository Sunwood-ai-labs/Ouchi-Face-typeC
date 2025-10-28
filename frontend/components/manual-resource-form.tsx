'use client';

import { FormEvent, useState } from 'react';

import { createManualResource } from '../lib/api';

export function ManualResourceForm() {
  const [status, setStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setStatus('Saving...');
    setError(null);

    const form = new FormData(event.currentTarget);
    const metadata: Record<string, unknown> = {
      kind: form.get('kind'),
      name: form.get('name'),
      description: form.get('description') || undefined,
      tags: (form.get('tags') as string)
        .split(',')
        .map((tag) => tag.trim())
        .filter(Boolean),
      url: form.get('url') || undefined,
      path: form.get('path') || undefined,
      repo: form.get('repo') || undefined,
      healthcheck: form.get('healthcheck') || undefined,
      owner: form.get('owner') || undefined,
      license: form.get('license') || undefined,
      thumbnail: form.get('thumbnail') || undefined
    };

    try {
      const resource = await createManualResource(metadata);
      setStatus(`Saved ${resource.name}!`);
      event.currentTarget.reset();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create resource');
      setStatus(null);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6 rounded-2xl border border-slate-800 bg-slate-900/60 p-8">
      <div className="grid gap-6 md:grid-cols-2">
        <label className="flex flex-col text-sm text-slate-200">
          Kind
          <select
            name="kind"
            required
            className="mt-2 rounded-md border border-slate-700 bg-slate-950 px-3 py-2 focus:border-primary-400 focus:outline-none"
          >
            <option value="app">App</option>
            <option value="dataset">Dataset</option>
            <option value="model">Model</option>
          </select>
        </label>
        <label className="flex flex-col text-sm text-slate-200">
          Name
          <input
            name="name"
            required
            className="mt-2 rounded-md border border-slate-700 bg-slate-950 px-3 py-2 focus:border-primary-400 focus:outline-none"
          />
        </label>
      </div>
      <label className="flex flex-col text-sm text-slate-200">
        Description
        <textarea
          name="description"
          rows={3}
          className="mt-2 rounded-md border border-slate-700 bg-slate-950 px-3 py-2 focus:border-primary-400 focus:outline-none"
        />
      </label>
      <div className="grid gap-6 md:grid-cols-2">
        <label className="flex flex-col text-sm text-slate-200">
          Tags (comma separated)
          <input
            name="tags"
            placeholder="nlp, dashboard"
            className="mt-2 rounded-md border border-slate-700 bg-slate-950 px-3 py-2 focus:border-primary-400 focus:outline-none"
          />
        </label>
        <label className="flex flex-col text-sm text-slate-200">
          URL
          <input
            name="url"
            type="url"
            placeholder="http://localhost:7860"
            className="mt-2 rounded-md border border-slate-700 bg-slate-950 px-3 py-2 focus:border-primary-400 focus:outline-none"
          />
        </label>
      </div>
      <div className="grid gap-6 md:grid-cols-2">
        <label className="flex flex-col text-sm text-slate-200">
          Filesystem path
          <input
            name="path"
            placeholder="/data/datasets/sample"
            className="mt-2 rounded-md border border-slate-700 bg-slate-950 px-3 py-2 focus:border-primary-400 focus:outline-none"
          />
        </label>
        <label className="flex flex-col text-sm text-slate-200">
          Repository URL
          <input
            name="repo"
            type="url"
            placeholder="https://forgejo.local/user/repo"
            className="mt-2 rounded-md border border-slate-700 bg-slate-950 px-3 py-2 focus:border-primary-400 focus:outline-none"
          />
        </label>
      </div>
      <div className="grid gap-6 md:grid-cols-3">
        <label className="flex flex-col text-sm text-slate-200">
          Healthcheck path
          <input
            name="healthcheck"
            placeholder="/health"
            className="mt-2 rounded-md border border-slate-700 bg-slate-950 px-3 py-2 focus:border-primary-400 focus:outline-none"
          />
        </label>
        <label className="flex flex-col text-sm text-slate-200">
          Owner
          <input
            name="owner"
            placeholder="@alice"
            className="mt-2 rounded-md border border-slate-700 bg-slate-950 px-3 py-2 focus:border-primary-400 focus:outline-none"
          />
        </label>
        <label className="flex flex-col text-sm text-slate-200">
          Thumbnail URL
          <input
            name="thumbnail"
            placeholder="https://..."
            className="mt-2 rounded-md border border-slate-700 bg-slate-950 px-3 py-2 focus:border-primary-400 focus:outline-none"
          />
        </label>
      </div>
      <div className="flex items-center justify-between">
        <div className="text-sm text-slate-400">
          {status ? <span className="text-emerald-300">{status}</span> : null}
          {error ? <span className="text-rose-300">{error}</span> : null}
        </div>
        <button
          type="submit"
          className="rounded-md bg-primary-600 px-4 py-2 font-semibold text-white hover:bg-primary-500"
        >
          Save resource
        </button>
      </div>
    </form>
  );
}
