/**
 * Форматирует число с разделителями тысяч для русской локали
 */
export function formatNumber(value: number, suffix: string = ''): string {
  return value.toLocaleString('ru-RU') + suffix;
} 