import { ProductRating as ProductRatingType } from '@/types';
import CountUp from './CountUp';

interface ProductRatingProps {
  rating: ProductRatingType;
}

export default function ProductRating({ rating }: ProductRatingProps) {
  const renderStars = (rating: number) => {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    const stars = [];

    for (let i = 0; i < fullStars; i++) {
      stars.push('★');
    }
    
    if (hasHalfStar && fullStars < 5) {
      stars.push('☆');
    }
    
    while (stars.length < 5) {
      stars.push('☆');
    }

    return stars.join('');
  };

  return (
    <div className="container max-w-4xl mx-auto my-4 bg-white rounded-xl shadow-lg p-6 text-gray-900">
      <div className="flex items-center gap-4 text-lg">
        <span className="text-gray-900">Рейтинг базы</span>
        <span className="font-bold text-gray-900">
          <CountUp 
            key={`rating-${rating.reviews_count}`}
            end={rating.average_rating} 
            formatNumber={false}
            duration={800}
            decimals={1}
          /> 
        </span>
        <span className="text-yellow-400 text-xl">
          {renderStars(rating.average_rating)}
        </span>
        <span className="text-gray-600">
          Оценок: <CountUp 
            key={`reviews-${rating.reviews_count}`}
            end={rating.reviews_count} 
            formatNumber={false}
            duration={600}
          />
        </span>
      </div>
    </div>
  );
} 