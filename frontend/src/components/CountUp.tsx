'use client';

import { useEffect, useState } from 'react';

interface CountUpProps {
  end: number;
  duration?: number;
  prefix?: string;
  suffix?: string;
  className?: string;
  formatNumber?: boolean;
  decimals?: number;
}

export default function CountUp({ 
  end, 
  duration = 1500, 
  prefix = '', 
  suffix = '', 
  className = '',
  formatNumber = true,
  decimals = 0
}: CountUpProps) {
  // ИСПРАВЛЕНО: Начинаем с конечного значения для SEO
  const [count, setCount] = useState(end);

  useEffect(() => {
    // Запускаем анимацию только на клиенте после гидратации
    let startTime: number | null = null;
    let animationFrame: number;

    const animate = (timestamp: number) => {
      if (!startTime) startTime = timestamp;
      const progress = Math.min((timestamp - startTime) / duration, 1);
      
      // Используем easeOut функцию для плавной анимации
      const easeOut = 1 - Math.pow(1 - progress, 3);
      const currentCount = easeOut * end;
      
      setCount(currentCount);

      if (progress < 1) {
        animationFrame = requestAnimationFrame(animate);
      }
    };

    // Небольшая задержка для лучшего UX
    const timeoutId = setTimeout(() => {
      setCount(0); // Сброс только для анимации
      animationFrame = requestAnimationFrame(animate);
    }, 200);

    return () => {
      if (animationFrame) {
        cancelAnimationFrame(animationFrame);
      }
      clearTimeout(timeoutId);
    };
  }, [end, duration]);

  const formatValue = (value: number) => {
    const rounded = decimals > 0 ? value.toFixed(decimals) : Math.floor(value);
    if (!formatNumber) return rounded.toString();
    if (decimals > 0) return parseFloat(rounded.toString()).toLocaleString('ru-RU');
    return Math.floor(value).toLocaleString('ru-RU');
  };

  return (
    <span className={className}>
      {prefix}{formatValue(count)}{suffix}
    </span>
  );
} 