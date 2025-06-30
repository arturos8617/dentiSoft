export function getCSRFToken(): string {
    if (typeof document === 'undefined') return '';
    const match = document.cookie.match(/(?:csrftoken|__Secure-csrftoken)=([^;]+)/);
    return match ? decodeURIComponent(match[1]) : '';
  }