interface ProductTagsProps {
  tags: string | null;
}

export default function ProductTags({ tags }: ProductTagsProps) {
  // Парсим строку тегов, разделенную запятыми
  const tagsList = tags ? tags.split(',').map(tag => tag.trim()).filter(tag => tag.length > 0) : [];

  if (tagsList.length === 0) {
    return null;
  }

  return (
    <div className="container max-w-4xl mx-auto my-4 bg-white rounded-xl shadow-lg p-6">
      <div className="flex flex-wrap gap-2">
        {tagsList.map((tag, index) => (
          <span
            key={index}
            className="inline-block bg-gray-100 text-gray-800 px-3 py-1 rounded-md text-sm"
          >
            {tag}
          </span>
        ))}
      </div>
    </div>
  );
} 