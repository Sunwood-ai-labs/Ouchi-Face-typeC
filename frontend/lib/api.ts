export type ResourceKind = 'app' | 'dataset' | 'model';

export interface Resource {
  id: number;
  kind: ResourceKind;
  name: string;
  slug: string;
  description?: string | null;
  tags: string[];
  url?: string | null;
  path?: string | null;
  repo_url?: string | null;
  owner?: string | null;
  thumbnail_path?: string | null;
  license?: string | null;
  healthcheck_path?: string | null;
  updated_at?: string | null;
  last_synced_at?: string | null;
  health_status: string;
  health_checked_at?: string | null;
  source: 'manual' | 'repository';
  created_at: string;
  modified_at: string;
}

export interface ResourceListResponse {
  items: Resource[];
  total: number;
}

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? 'http://localhost:8000';

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const message = await res.text();
    throw new Error(message || 'Failed to communicate with API');
  }
  return res.json() as Promise<T>;
}

export async function fetchResources(params: {
  kind?: ResourceKind;
  q?: string;
  tag?: string;
  owner?: string;
  limit?: number;
  offset?: number;
} = {}): Promise<ResourceListResponse> {
  const search = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      search.set(key, String(value));
    }
  });
  const url = `${API_BASE}/api/resources${search.toString() ? `?${search.toString()}` : ''}`;
  const res = await fetch(url, { next: { revalidate: 30 } });
  return handleResponse<ResourceListResponse>(res);
}

export async function fetchResource(id: number): Promise<Resource> {
  const res = await fetch(`${API_BASE}/api/resources/${id}`, { next: { revalidate: 30 } });
  return handleResponse<Resource>(res);
}

export async function fetchResourceBySlug(slug: string): Promise<Resource> {
  const res = await fetch(`${API_BASE}/api/resources/slug/${slug}`, { next: { revalidate: 30 } });
  return handleResponse<Resource>(res);
}

export async function createManualResource(metadata: Record<string, unknown>): Promise<Resource> {
  const res = await fetch(`${API_BASE}/api/resources`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ source_type: 'manual', metadata })
  });
  return handleResponse<Resource>(res);
}
