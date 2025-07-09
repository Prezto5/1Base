'use client';

import { RegionInfo } from '@/types';
import { useRouter } from 'next/navigation';

interface RegionSelectorProps {
  regions: RegionInfo[];
  currentRegionSlug: string;
  productSlug: string;
}

export default function RegionSelector({ 
  regions, 
  currentRegionSlug, 
  productSlug 
}: RegionSelectorProps) {
  const router = useRouter();

  const handleRegionChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const newRegionSlug = event.target.value;
    router.push(`/${productSlug}/${newRegionSlug}`);
  };

  return (
    <div className="mb-4">
      <label htmlFor="region-select" className="block text-sm font-medium mb-2 text-gray-900">
        Регион:
      </label>
      <select
        id="region-select"
        value={currentRegionSlug}
        onChange={handleRegionChange}
        className="w-full md:w-auto px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent text-gray-900 bg-white"
      >
        {regions.map((region) => (
          <option key={region.slug} value={region.slug} className="text-gray-900">
            {region.name_nominative}
          </option>
        ))}
      </select>
    </div>
  );
} 