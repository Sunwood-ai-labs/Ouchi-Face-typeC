import { ResourceCard } from '../../components/resource-card';
import { ResourceFilterBar } from '../../components/resource-filter-bar';
import { fetchResources, ResourceKind } from '../../lib/api';

type SearchParams = {
  kind?: ResourceKind;
  q?: string;
  tag?: string;
  owner?: string;
};

export default async function BrowsePage({ searchParams }: { searchParams: SearchParams }) {
  const params = {
    kind: searchParams.kind,
    q: searchParams.q,
    tag: searchParams.tag,
    owner: searchParams.owner
  };
  const { items, total } = await fetchResources(params);

  return (
    <section className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-slate-100">Browse the catalog</h1>
        <p className="mt-2 text-slate-300">Use the filters to slice your homelab knowledge base however you like.</p>
      </div>
      <ResourceFilterBar
        initialKind={params.kind ?? ''}
        initialQuery={params.q ?? ''}
        initialTag={params.tag ?? ''}
        initialOwner={params.owner ?? ''}
      />
      <div className="flex items-center justify-between text-sm text-slate-400">
        <span>{total} resources</span>
        <a href="/admin/new" className="text-primary-300 hover:text-primary-200">
          + Register new resource
        </a>
      </div>
      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
        {items.length ? (
          items.map((resource) => <ResourceCard key={resource.id} resource={resource} />)
        ) : (
          <p className="rounded-lg border border-dashed border-slate-700 p-6 text-sm text-slate-400">
            Nothing found. Try adjusting your filters or syncing repos.
          </p>
        )}
      </div>
    </section>
  );
}
