/**
 * Utility functions for consistent number formatting across the application
 */

/**
 * Format a number to a maximum of 2-3 decimal places
 * @param {number|string} value - The value to format
 * @param {number} maxDecimalPlaces - Maximum decimal places (default: 2)
 * @param {boolean} removeTrailingZeros - Remove trailing zeros (default: true)
 * @returns {string} - Formatted number string
 */
export const formatNumber = (value, maxDecimalPlaces = 2, removeTrailingZeros = true) => {
  if (value === null || value === undefined || value === '') {
    return '0';
  }
  
  const num = typeof value === 'string' ? parseFloat(value) : value;
  
  if (isNaN(num) || !isFinite(num)) {
    return '0';
  }
  
  let formatted = num.toFixed(maxDecimalPlaces);
  
  if (removeTrailingZeros) {
    // Remove trailing zeros and decimal point if not needed
    formatted = formatted.replace(/\.?0+$/, '');
  }
  
  return formatted;
};

/**
 * Format a percentage value
 * @param {number|string} value - The value to format as percentage
 * @param {number} maxDecimalPlaces - Maximum decimal places (default: 1)
 * @returns {string} - Formatted percentage string
 */
export const formatPercentage = (value, maxDecimalPlaces = 1) => {
  const formatted = formatNumber(value, maxDecimalPlaces);
  return `${formatted}%`;
};

/**
 * Format a temperature value
 * @param {number|string} value - The temperature value
 * @param {string} unit - Temperature unit (default: '°C')
 * @param {number} maxDecimalPlaces - Maximum decimal places (default: 1)
 * @returns {string} - Formatted temperature string
 */
export const formatTemperature = (value, unit = '°C', maxDecimalPlaces = 1) => {
  const formatted = formatNumber(value, maxDecimalPlaces);
  return `${formatted}${unit}`;
};

/**
 * Format an anomaly score (0-1 range)
 * @param {number|string} score - The anomaly score
 * @param {number} maxDecimalPlaces - Maximum decimal places (default: 3)
 * @returns {string} - Formatted anomaly score
 */
export const formatAnomalyScore = (score, maxDecimalPlaces = 3) => {
  if (typeof score === 'number') {
    if (isNaN(score) || !isFinite(score)) {
      return '0.000';
    }
    return score.toFixed(maxDecimalPlaces);
  }
  if (typeof score === 'string') {
    const parsed = parseFloat(score);
    return isNaN(parsed) ? '0.000' : parsed.toFixed(maxDecimalPlaces);
  }
  return '0.000';
};

/**
 * Format a currency value
 * @param {number|string} value - The currency value
 * @param {string} currency - Currency symbol (default: '$')
 * @param {number} maxDecimalPlaces - Maximum decimal places (default: 2)
 * @returns {string} - Formatted currency string
 */
export const formatCurrency = (value, currency = '$', maxDecimalPlaces = 2) => {
  const formatted = formatNumber(value, maxDecimalPlaces, false); // Don't remove trailing zeros for currency
  return `${currency}${formatted}`;
};

/**
 * Format a metric value with units
 * @param {number|string} value - The metric value
 * @param {string} unit - The unit (e.g., 'kg', 'L', 'm')
 * @param {number} maxDecimalPlaces - Maximum decimal places (default: 2)
 * @returns {string} - Formatted metric string
 */
export const formatMetric = (value, unit = '', maxDecimalPlaces = 2) => {
  const formatted = formatNumber(value, maxDecimalPlaces);
  return unit ? `${formatted} ${unit}` : formatted;
};

/**
 * Format a large number with appropriate suffixes (K, M, B)
 * @param {number|string} value - The value to format
 * @param {number} maxDecimalPlaces - Maximum decimal places (default: 1)
 * @returns {string} - Formatted number with suffix
 */
export const formatLargeNumber = (value, maxDecimalPlaces = 1) => {
  const num = typeof value === 'string' ? parseFloat(value) : value;
  
  if (isNaN(num) || !isFinite(num)) {
    return '0';
  }
  
  const absNum = Math.abs(num);
  
  if (absNum >= 1e9) {
    return `${formatNumber(num / 1e9, maxDecimalPlaces)}B`;
  } else if (absNum >= 1e6) {
    return `${formatNumber(num / 1e6, maxDecimalPlaces)}M`;
  } else if (absNum >= 1e3) {
    return `${formatNumber(num / 1e3, maxDecimalPlaces)}K`;
  } else {
    return formatNumber(num, maxDecimalPlaces);
  }
};

/**
 * Format a file size in bytes to human readable format
 * @param {number} bytes - Size in bytes
 * @param {number} maxDecimalPlaces - Maximum decimal places (default: 1)
 * @returns {string} - Formatted file size
 */
export const formatFileSize = (bytes, maxDecimalPlaces = 1) => {
  if (bytes === 0) return '0 B';
  
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return `${formatNumber(bytes / Math.pow(k, i), maxDecimalPlaces)} ${sizes[i]}`;
};

/**
 * Parse and format a number ensuring it's within specified decimal places
 * @param {any} value - Value to parse and format
 * @param {number} maxDecimalPlaces - Maximum decimal places (default: 2)
 * @returns {number} - Parsed and formatted number
 */
export const parseAndFormatNumber = (value, maxDecimalPlaces = 2) => {
  const num = typeof value === 'string' ? parseFloat(value) : value;
  
  if (isNaN(num) || !isFinite(num)) {
    return 0;
  }
  
  return parseFloat(num.toFixed(maxDecimalPlaces));
};
