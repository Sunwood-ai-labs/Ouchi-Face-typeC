import { ManualResourceForm } from '../../../components/manual-resource-form';

export default function NewResourcePage() {
  return (
    <section className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-slate-100">Register a resource</h1>
        <p className="mt-2 max-w-2xl text-slate-300">
          Paste URLs, dataset paths, or repo metadata from ouchi.yaml. You can sync repositories later from the detail view.
        </p>
      </div>
      <ManualResourceForm />
    </section>
  );
}
