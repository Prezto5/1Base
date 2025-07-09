export default function ProductTags() {
  const tags = [
    'рестораны',
    'кафе', 
    'гостиницы',
    'базы отдыха',
    'отели',
    'бары',
    'клубы',
    'столовые',
    'хорека'
  ];

  return (
    <div className="container max-w-4xl mx-auto my-4 bg-white rounded-xl shadow-lg p-6">
      <div className="flex flex-wrap gap-2">
        {tags.map((tag, index) => (
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