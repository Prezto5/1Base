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
  const [count, setCount] = useState(0);

  useEffect(() => {
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

    // Сброс счетчика и запуск анимации
    setCount(0);
    animationFrame = requestAnimationFrame(animate);

    return () => {
      if (animationFrame) {
        cancelAnimationFrame(animationFrame);
      }
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